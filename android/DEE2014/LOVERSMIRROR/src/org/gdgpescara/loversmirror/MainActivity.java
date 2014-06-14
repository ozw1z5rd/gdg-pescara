package org.gdgpescara.loversmirror;

import org.gdgpescara.loversmirror.R;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Point;
import android.os.Bundle;
import android.util.Log;
import android.view.Display;
import android.view.MenuInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.ValueEventListener;
import com.firebase.client.FirebaseError;

public class MainActivity extends Activity {
	final static int MAXTOUCHES = 10;
	final static String TAG = "LOVERSMIRROR";

	// Queste url sono associate ad un account free!
	final static String FIREBASE_URL_ME = "https://sweltering-fire-220.firebaseio.com/me"; 
	final static String FIREBASE_URL_YOU = "https://sweltering-fire-220.firebaseio.com/you";
	// Posizione dita schermo remoto
	private float[] rX = new float[MAXTOUCHES];
	private float[] rY = new float[MAXTOUCHES];
	private int remoteCircleToDraw = 0;
	
	private int radius;
	
	// strutture descrittive della modalità di disegno delle dita locali e remote
	private Paint circlePaint = new Paint();
	private Paint remoteCirclePaint = new Paint();

	private Firebase firebasea = new Firebase(FIREBASE_URL_ME);
	private Firebase firebaseb = new Firebase(FIREBASE_URL_YOU);
	
	private Firebase firebaseme = null;
	private Firebase firebaseyou = null;
	
	private float displayW;
	private float displayH;
	
	ValueEventListener valueEventListener;
	
	DrawingView dv;
	
	protected void setupCirclePaint() {
		circlePaint.setAntiAlias(true);
		circlePaint.setColor(Color.BLUE);
		circlePaint.setStyle(Paint.Style.STROKE);
		circlePaint.setStrokeJoin(Paint.Join.MITER);
		circlePaint.setStrokeWidth(4f);
		remoteCirclePaint.setAntiAlias(true);
		remoteCirclePaint.setColor(Color.RED);
		remoteCirclePaint.setStyle(Paint.Style.STROKE);
		remoteCirclePaint.setStrokeJoin(Paint.Join.MITER);
		remoteCirclePaint.setStrokeWidth(5f);
	}
	
	//
	// xxxxyyyy <-- 8 caratteri per posizione
	// n x 8 caratteri quando si tracciano n dita
	// vedi anche syncronizeStateWithRemote()
	//
	protected void setupFirebase() {
		valueEventListener = new ValueEventListener() {
			@Override
			public void onDataChange(DataSnapshot snap) {
		    	String message = String.format("%s",snap.getValue());
		    	Log.i(TAG, message );
		    	int length = message.length();
		    	if ( length > 0 ) {
		    		//Log.i(TAG, String.format(">>>> %s",message));
		    		remoteCircleToDraw = length / 8;
		    		//Log.i(TAG,String.format("got %d circle to draw",remoteCircleToDraw));
		    		int j,i;
		    		for ( i = j = 0; i < length; i += 8, j++ ) {
		    			rX[j] = Integer.parseInt( 
		    				message.substring(i,i+4)
		    					)/10000.0f*displayW;
		    			rY[j] = Integer.parseInt( 
		    				message.substring(i+4,i+8)
		    					)/10000.0f*displayH;
		    		}
		    	} 
		    	else { 
		    		remoteCircleToDraw = 0;
		    	}
		    	//force view redraw ( when invalid onDraw is called )
			    dv.invalidate();
			}

			@Override public void onCancelled(FirebaseError error) { }
		};
		
		firebaseyou.addValueEventListener( valueEventListener );
	}
	
	
	private int getRadiusValue( ) {
		Display display = getWindowManager().getDefaultDisplay();
		Point size = new Point();
		display.getSize( size );
		return Math.min(size.x, size.y) / 10;
	}
	
	// Viene chiamato un tantum dal sistema per produrre il menu 
	// per questa applicazione, ma se viene reso invalido con 
	// invalidateMenuOptions, il sistema sarà costretto a 
	// chiamarla di nuovo.
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.activity_main, menu);
		if ( firebaseyou != null ) {
			menu.findItem(R.id.idSetAsA).setVisible(false);
			menu.findItem(R.id.idSetAsAB).setVisible(false);
			menu.findItem(R.id.idSetAsB).setVisible(false);
		}
		return true;//ritorna true in modo da visualizzare il menu
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		
		case R.id.idSetAsA:
			firebaseme = firebasea;
			firebaseyou = firebaseb;
			setupFirebase();
			invalidateOptionsMenu();
			break;
		
		case R.id.idSetAsB:
			firebaseme = firebaseb;
			firebaseyou = firebasea;
			setupFirebase();
			invalidateOptionsMenu();
			break;

		case R.id.idSetAsAB:
			firebaseme = firebasea;
			firebaseyou = firebasea;
			setupFirebase();
			invalidateOptionsMenu();
			break;
			
		case R.id.idFine:
			finish();
			break;
		}
	    return super.onOptionsItemSelected(item);
	}   
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		dv = new DrawingView(this);
		radius = getRadiusValue();
		setContentView(dv);
		setupCirclePaint();
		// inizializzazione del canale è fatto attraverso il menu
		// setupFirebase();
	}


	//
	// Questa è ad uso interno, riceve gli eventi touch e disegna sullo schermo
	//
	public class DrawingView extends View {
		public int width;
		public int height;
		private Bitmap mBitmap;
		private Canvas mCanvas;
		private Paint mBitmapPaint;
		private Path circlePath;
		private Path remoteCirclePath;
		private int circleToDraw = 0;
		private int oldCircleToDraw = 0;
		// posizioni correnti
		private float[] mX = new float[MAXTOUCHES];
		private float[] mY = new float[MAXTOUCHES];
		private static final float TOUCH_TOLERANCE = 4;

		public DrawingView(Context context) {
			super(context);
			mBitmapPaint = new Paint(Paint.DITHER_FLAG);
			circlePath = new Path();
			remoteCirclePath = new Path();
		}

		//
		// Display ruotato, tiene traccia della nuova dimensione in modo
		// da inviare al remoto sempre dati normalizzati
		//
		@Override
		protected void onSizeChanged(int w, int h, int oldw, int oldh) {
			super.onSizeChanged(w, h, oldw, oldh);
			displayH = h;
			displayW = w;
			mBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
			mCanvas = new Canvas(mBitmap);
		}

		//
		// Chiamato quando la view deve essere ridisegnata
		//
		@Override
		protected void onDraw(Canvas canvas) {
			super.onDraw(canvas);
			canvas.drawBitmap(mBitmap, 0, 0, mBitmapPaint);
			circlePath.reset();
			remoteCirclePath.reset();
			
			for (int i = 0; i < circleToDraw; i++)
				circlePath.addCircle(mX[i], mY[i], radius, Path.Direction.CW);
			
			for (int i = 0; i < remoteCircleToDraw; i++)
				remoteCirclePath.addCircle(rX[i], rY[i], radius, Path.Direction.CW);
			
			canvas.drawPath(circlePath, circlePaint);
			canvas.drawPath(remoteCirclePath, remoteCirclePaint);
			syncronizeStateWithRemote();
		}

		private void syncronizeStateWithRemote() {
			// aspetta per l'inzializzazione dei canali
			if ( firebaseme == null )
				return;
			
			StringBuffer message = new StringBuffer("");
			for ( int i = 0 ; i < circleToDraw; i++) {
				message.append(
					String.format("%04d%04d", 
						(int)(mX[i]/displayW*10000), 
						// qualche volta mY > displayH
						(int)(mY[i]/(1+Math.max(mY[i],displayH))*10000) 
					)
				);
			}
			firebaseme.setValue(message);
		}

		private void touch_start(int index, float x, float y) {
			mX[index] = x;
			mY[index] = y;
		}

		private void touch_move(int index, float x, float y) {
			float dx = Math.abs(x - mX[index]);
			float dy = Math.abs(y - mY[index]);
			if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
				mX[index] = x;
				mY[index] = y;
			}
		}

		private void touch_up() {
			circlePath.reset();
			circleToDraw = 0;
			syncronizeStateWithRemote();
		}

		@Override
		public boolean onTouchEvent(MotionEvent event) {
			int action = event.getAction() & MotionEvent.ACTION_MASK;
			int pointerIndex = (event.getAction() & MotionEvent.ACTION_POINTER_INDEX_MASK) >> MotionEvent.ACTION_POINTER_INDEX_SHIFT;

			int pointerCount = event.getPointerCount();
			circleToDraw = pointerCount;
			for (int i = 0; i < pointerCount; i++) {
				if (event.getAction() != MotionEvent.ACTION_MOVE
						&& i != pointerIndex) {
					// if it's an up/down/cancel/out event, mask the id to see
					// if we should process it for this touch point
					continue;
				}
				// int pointerId = event.getPointerId(i);

				float x = event.getX(i);
				float y = event.getY(i);
				switch (action) {
				case MotionEvent.ACTION_DOWN:
				case MotionEvent.ACTION_POINTER_DOWN:
					touch_start(i, x, y);
					invalidate();
					break;
				case MotionEvent.ACTION_MOVE:
					touch_move(i, x, y);
					invalidate();
					break;
				case MotionEvent.ACTION_UP:
				case MotionEvent.ACTION_POINTER_UP:
				case MotionEvent.ACTION_OUTSIDE:
				case MotionEvent.ACTION_CANCEL:
					touch_up();
					invalidate();
					break;
				}
			} // for
			return true;
		} // method
	} // drawingView
} // MainActivity
