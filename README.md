# DaChuang
The path.py is for plan the path of the plan  

## Begin
At first, we need to input three GPS points of the box and the a GPS point of the start.

## First point 
The first point we will go should be the closest point to the start point.

## Second point
From the first point to the second point, I want the plane can fly along a Straight. To reduce the error, I let the plane fly alone an arc when it fly to the first point.  
For the arc, it begin at the start point and end at the first point. The tangent line of the arc at the first point will pass the second point.  
And also to reduce the error, the radius of the arc should as large as possible, so we also need to choice a point as the second point.

## Last point 
When the plane arrive the second point, the fly will enter the next arc to the third point, the arc have two tangent lines at second and third lines which are intersectant at the first point.

## After recognition  
After recognition, we will calculate which point to fight.     
* **If is the first point**, the plane will fly along the straight.  
* **If is the second point**, the plane will fly along the second arc to the point 2.  
* **If is the third point**, The plane will fly along the third arc to the point 3, or the plane also an change the post to perpendicular to the ground and back to the point 3.
