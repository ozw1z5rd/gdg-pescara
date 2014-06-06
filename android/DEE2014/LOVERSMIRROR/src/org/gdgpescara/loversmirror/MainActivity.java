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

public class MainActivity extends Activity {
	final static int MAXTOUCHES = 10;
	final static String TAG = "DEMO";
	private  Paint circlePaint = new Paint();

	protected void setupCirclePaint( ) {
       circlePaint.setAntiAlias(true);
       circlePaint.setColor(Color.BLUE);
       circlePaint.setStyle(Paint.Style.STROKE);
       circlePaint.setStrokeJoin(Paint.Join.MITER);
       circlePaint.setStrokeWidth(4f);		
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
	   super.onCreate(savedInstanceState);
	   DrawingView dv = new DrawingView(this);
	   setContentView(dv);
	   setupCirclePaint();
	}
	
	//
	// Questa è ad uso interno, riceve gli eventi touch e disegna sullo schermo
	//
	public class DrawingView extends View {
	
	       public  int width;
	       public  int height;
	       private Bitmap mBitmap;
	       private Canvas mCanvas;
	       private Paint mBitmapPaint;
	       private Path circlePath;
	       private int circleToDraw = 0;
	       private float[] mX = new float[MAXTOUCHES];
	       private float[] mY = new float[MAXTOUCHES];
	       private static final float TOUCH_TOLERANCE = 4;
	       
	       public DrawingView(Context c) {
		       super(c);
		       mBitmapPaint = new Paint(Paint.DITHER_FLAG);
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
		       circlePath.reset();
		       for ( int i = 0 ; i < circleToDraw; i++ ) {
		    	   circlePath.addCircle(mX[i], mY[i], 100, Path.Direction.CW);
		       }
		       canvas.drawPath( circlePath,  circlePaint);
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
	       }
	
	       @Override
	       public boolean onTouchEvent(MotionEvent event) {
	   			int action = event.getAction() & MotionEvent.ACTION_MASK;
	   			Log.i(TAG,String.format("%d <---", action));
	   			// indice del cursore che si è mosso ? 
	   			int pointerIndex = ( event.getAction() & 
	   					MotionEvent.ACTION_POINTER_INDEX_MASK ) >> 
	   					    MotionEvent.ACTION_POINTER_INDEX_SHIFT;
	   					    
	   			int pointerCount = event.getPointerCount();
	   			circleToDraw = pointerCount;
	   			for (int i = 0; i < pointerCount; i++) {
	   				if ( event.getAction() != MotionEvent.ACTION_MOVE && 
	   					 i != pointerIndex) {
	   					// if it's an up/down/cancel/out event, mask the id to see if we should	process it for this touch point
	   					continue;
	   				}
	   				//int pointerId = event.getPointerId(i);    	   
	    	   
			        float x = event.getX(i);
			        float y = event.getY(i);
			
			        switch ( action ) {
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
	   			} 
	       return true;
	       }  
	   }
	 }
