package org.gdgpescara.loversmirror;

import java.util.ArrayList;
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

public class MainActivity extends Activity {
	
	//
	// visibile nella classe DrawingView ed impostata su onCreate
	// 
		private Paint	mPaint;
	// 
	// al più ci possono essere 10 dita sullo schermo
	// che vengono mosse contemporaneamente
	//
	final static int MAXTOUCHES = 10;
	//
	// Stringa per identificazione log
	//
	final static String TAG = "DEMO";
	
	//
	// conserviamo al max posizione per 10 dita
	// ( impossibile ) 
	//
	float[] x  = new float[10];
	float[] y  = new float[10];
	int[]   id = new int[10];
	
	// true se il dito i-esimo poggia sullo schermo
	boolean[] down = new boolean[10];
	
	// 10 impostazioni differenti di disegno per i 10 cerchi
	private  ArrayList<Paint> circlePaints = new ArrayList<Paint>(10);


	protected void setupCirclesPaints( ) {
		for ( int i = 0 ; i < MAXTOUCHES; i++ ) {
			Log.i(TAG, String.format("Indice corrente: %d\n", i));
			   circlePaints.add( new Paint() );
		       circlePaints.get(i).setAntiAlias(true);
		       circlePaints.get(i).setColor(Color.BLUE);
		       circlePaints.get(i).setStyle(Paint.Style.STROKE);
		       circlePaints.get(i).setStrokeJoin(Paint.Join.MITER);
		       circlePaints.get(i).setStrokeWidth(4f);		
		}
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
	   super.onCreate(savedInstanceState);
	   
	   DrawingView dv = new DrawingView(this);
	   setContentView(dv);
	   
	   for ( int i = 0 ; i < MAXTOUCHES; i++ ) {
		   x[i] = 0.0f; y[i]= 0.0f; id[i] = 0;
		   down[i] = false;
	   }
	   
	   setupCirclesPaints();
	}
	
	//
	// Questa è ad uso interno, riceve gli eventi touch e disegna sullo schermo
	//
	public class DrawingView extends View {
	
	       public 	int		width;
	       public 	int 	height;
	       private 	Bitmap  mBitmap;
	       private 	Canvas  mCanvas;
	       private 	Paint   mBitmapPaint;
	       			Context context;
	       private 	Path 	circlePath;
	       
	       
	       public DrawingView(Context c) {
		       super(c);
		       
		       context = c;
		       //
		       // Lista posizioni per linee tracciate a mano.
		       //
		       mBitmapPaint = new Paint(Paint.DITHER_FLAG);
		       
		       //
		       // Il circlePath è una lista di oggetti che vanno disegnati sulla bitmap
		       // con modalità circlePaint
		       //
		       circlePath = new Path();
	       }
	
	       //
	       // Display ruotato, 
	       // 
	       @Override
	       protected void onSizeChanged(int w, int h, int oldw, int oldh) {
		       super.onSizeChanged(w, h, oldw, oldh);
		       mBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
		       mCanvas = new Canvas(mBitmap);
	       }
	       //
	       // Chiamato quando la view deve essere ridisegnata
	       //
	       @Override
	       protected void onDraw(Canvas canvas) {
		       super.onDraw(canvas);
		       canvas.drawBitmap( mBitmap, 0, 0, mBitmapPaint);
		       canvas.drawPath( circlePath,  circlePaints.get(0));
	       }
	
	       private float mX, mY;
	       
	       private static final float TOUCH_TOLERANCE = 4;
	
	       //
	       // 
	       //
	       private void touch_start(float x, float y) {
	    	   mX = x;
	    	   mY = y;
	       }
	       
	       //
	       // Touch mosso 
	       //
	       private void touch_move(float x, float y) {
	       float dx = Math.abs(x - mX);
	       float dy = Math.abs(y - mY);
	       if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
	           mX = x;
	           mY = y;
	           // cancella il cerchio precedente.
	           circlePath.reset();
	           // aggiunge il nuovo
	           circlePath.addCircle(mX, mY, 30, Path.Direction.CW);
	       }
	       }
	       
	       //
	       // Touch rilasciato
	       //
	       private void touch_up() {
	    	   circlePath.reset();
	    	   // commit the path to our offscreen
	    	   // kill this so we don't double draw
	       }
	
	       //
	       // Permette alla vista di gestire gli eventi Touch 
	       // calcola posizioni ed offset e disegna sulla bitmap
	       // Questo si avvia dal primo touch
	       //
	       //
	       @Override
	       public boolean onTouchEvent(MotionEvent event) {
	    	   
	   			Log.d(TAG, "Chiamata ad onTouch... ");
	   			int action = event.getAction() & MotionEvent.ACTION_MASK;
	   			// indice del cursore che si è mosso ? 
	   			int pointerIndex = (event.getAction() & MotionEvent.ACTION_POINTER_ID_MASK) >> 	MotionEvent.ACTION_POINTER_ID_SHIFT;
	   			// e questo che roba è ? 
	   			int pointerCount = event.getPointerCount();
	   			
	   			for (int i = 0; i < 10; i++) {
	   				if (i >= pointerCount) {
	   					down[i] = false;
	   					id[i] = -1;
	   					continue;
	   				}
	   				if ( event.getAction() != MotionEvent.ACTION_MOVE && i != pointerIndex) {
	   					// if it's an up/down/cancel/out event, mask the id to see if we should	process it for this touch point
	   					continue;
	   				}
	   				// recupera il puntatore i-esimo
	   				int pointerId = event.getPointerId(i);    	   
	    	   
	   				// per ogni puntatore gestisce il movimento 
	   				// del cerchio sullo schermo.
			        float x = event.getX();
			        float y = event.getY();
			
			        switch (event.getAction()) {
			           case MotionEvent.ACTION_DOWN:
			               touch_start(x, y);
			               invalidate();
			               break;
			           case MotionEvent.ACTION_MOVE:
			               touch_move(x, y);
			               invalidate();
			               break;
			           case MotionEvent.ACTION_UP:
			               touch_up();
			               invalidate();
			               break;
			        }
	   			} // fine del ciclo sui puntatori
	       return true;
	       }  
	   }
	 }
