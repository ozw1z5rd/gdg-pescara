package org.gdgpescara.loversmirror;


import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.ValueEventListener;
import com.firebase.client.FirebaseError;

public class MainActivity extends Activity {
	final static int MAXTOUCHES = 10;
	final static String TAG = "DEMO";

	final static String FIREBASE_URL_ME = "https://sweltering-fire-220.firebaseio.com/me"; 
	final static String FIREBASE_URL_YOU = "https://sweltering-fire-220.firebaseio.com/you";
	private float[] rX = new float[MAXTOUCHES];
	private float[] rY = new float[MAXTOUCHES];

	private int remoteCircleToDraw = 0;
	private Paint circlePaint = new Paint();
	private Paint remoteCirclePaint = new Paint();

	private Firebase firebaseme = new Firebase(FIREBASE_URL_ME);
	private Firebase firebaseyou = new Firebase(FIREBASE_URL_YOU);
	private float displayW;
	private float displayH;
	
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

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		DrawingView dv = new DrawingView(this);
		setContentView(dv);
		setupCirclePaint();

		rX[0] = 100.0f;
		rY[0] = 100.0f;
		remoteCircleToDraw = 1;
		
		firebaseme.addValueEventListener(new ValueEventListener() {

		    @Override
		    public void onDataChange(DataSnapshot snap) {
		    	String pos[] = new String[2];
		    	String stringSplit[] = new String[MAXTOUCHES+1];
		    	String message = String.format("%s",snap.getValue());
		    	if ( message.length() > 0 && ! message.equals("null") 
		    			&& ! message.equals("C:0")) {
		    		Log.i(TAG, String.format(">>>> %s",message));
		    		stringSplit = message.split("\\|");
		    		if ( stringSplit.length > 0) {
			    		remoteCircleToDraw = Integer.parseInt(stringSplit[0].substring(2));// c:<xx
			    		Log.i(TAG,String.format("got %d circle to draw",remoteCircleToDraw));
			    		for ( int i = 0; i < stringSplit.length - 1; i++ ) {
			    			Log.i(TAG, stringSplit[i+1]);
			    			pos = stringSplit[i+1].split(";");
			    			rX[i] = Integer.parseInt(pos[0])/10000.0f*displayW;
			    			rY[i] = Integer.parseInt(pos[1])/10000.0f*displayH;
			    		}
		    		}
		    		Log.i(TAG, message);
		    	}
		    }

		    @Override public void onCancelled(FirebaseError error) { }
		});
		
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
		private float[] mX = new float[MAXTOUCHES];
		private float[] mY = new float[MAXTOUCHES];
		private float[] oX = new float[MAXTOUCHES];
		private float[] oY = new float[MAXTOUCHES];
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
			for (int i = 0; i < circleToDraw; i++) {
				circlePath.addCircle(mX[i], mY[i], 100, Path.Direction.CW);
			}
			for (int i = 0; i < remoteCircleToDraw; i++) {
				remoteCirclePath
						.addCircle(rX[i], rY[i], 100, Path.Direction.CW);
			}
			canvas.drawPath(circlePath, circlePaint);
			canvas.drawPath(remoteCirclePath, remoteCirclePaint);
			syncronizeStateWithRemote();
		}

		// controlla se il numero dei cerchi oppure la loro posizione è variata
		// e nel caso invia di nuovo al remoto tutto lo stato locale
		// si potrebbe ottimizzare inviando solo le diffenze
		private void syncronizeStateWithRemote() {
			boolean alteredState = false;
			if (circleToDraw != oldCircleToDraw) {
				oldCircleToDraw = circleToDraw;
				alteredState = true;
			} else {
				for (int i = 1; i < circleToDraw; i++) {
					if (mX[i] != oX[i]) {
						alteredState = true;
						break;
					}
				}
			}
			// here altered state is available and updated
			if (alteredState) {
				StringBuffer message = new StringBuffer();
				message.append(String.format("C:%d", circleToDraw));
				for ( int i = 0 ; i < circleToDraw; i++) {
					message.append(
						String.format("|%04d;%04d", 
							(int)(mX[i]/displayW*10000), 
							(int)(mY[i]/displayH*10000) 
						)
					);
				}
				firebaseme.setValue(message);
			}
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
			circleToDraw--;
			syncronizeStateWithRemote();
		}

		@Override
		public boolean onTouchEvent(MotionEvent event) {
			int action = event.getAction() & MotionEvent.ACTION_MASK;
			// indice del cursore che si è mosso ?
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
