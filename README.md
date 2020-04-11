# MathVision

Mathematical Tools for Computer Vision

HW_5: RigidBody Rotation

![picture](demo.png)

Homework code is HW5_Code.cs. If you want to test this code, add the following script to the Assets folder and attach to an empty gameObject. 

In RigidBody\ Rotation/Assets/Scripts/compute_user_rotation.cs, you can find the modified version used for this demo.

You can try the demo by downloading the Matrix_rotation_demo file. Note that it was built on OSX. Make sure to set the Graphics Quality to "Ultra" as low quality makes objects disappear/reappear.

Alternatively, you can open Unity and navigate to RigidBody\ Rotation/Assets/Scenes/space_matrix_rotation to try the demo.

The demo is very straightforward. Just drag the earth around with your mouse to change the position of p1, p2 and p3. The compute_user_rotation.cs will compute the difference and update the meteor's position accordingly.