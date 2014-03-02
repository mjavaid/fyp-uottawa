#include<iostream>
#include<opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265

using namespace std;
using namespace cv;

CvCapture  * cam_input = NULL;

struct CloudPoint {
    int col, row;
    float X, Y, Z;

    int height;
    CloudPoint(int c, int r, float x, float y, float z, int h)
    : col(c), row(r), X(x), Y(y), Z(z), height(h) {}
    CloudPoint() {}
};

struct MeasureResult {
    float distance;
    float yaw;
    float pitch;
};

// FUNCTION PROTOTYPES
float findLaserCenterByRow(unsigned char * row, size_t rowsz);
void calcDistanceByPos( float x, int y, int img_height, MeasureResult *result);

int main() {

    const int IMAGE_HEIGHT = 480;
    const int cloud_pt_row_delta = 1;

    int opt_start_angle10 = 10;
    int opt_end_angle10   = 1800;
    int opt_angle_stepping10 = 5;
    
    bool opt_show_help =false;
    //const char * cloudpoint_file = NULL;
    int cameraID = 0;

    int pos = 1;
    cam_input = cvCaptureFromCAM(0);

    int cloud_pt_row_num = IMAGE_HEIGHT/cloud_pt_row_delta;
    FILE * dumpfile;
    IplImage* currentFrame;
    IplImage* undistorted;
    IplImage* grayFrame;
    CvSize frameSz;

    currentFrame = cvQueryFrame(cam_input);
	//currentFrame = cvQueryFrame(cam_input);
    frameSz.height = currentFrame->height;
    frameSz.width  = currentFrame->width;

    currentFrame = cvQueryFrame(cam_input);
	IplImage* cloned=cvCloneImage(currentFrame);
    
    int currentAngle10 = opt_start_angle10;

    float * laserDotArr = new float[frameSz.height];
    grayFrame = cvCreateImage(cvSize(frameSz.width, frameSz.height),IPL_DEPTH_8U, 1);
    undistorted = cvCreateImage(cvSize(frameSz.width,frameSz.height), IPL_DEPTH_8U, 3);
       
    //if (cloudpoint_file)
    dumpfile = fopen("dumpfile.txt", "w");

    MeasureResult result = { 0, 0, 0};

    CloudPoint * cloudpt_col = new CloudPoint[cloud_pt_row_num];

    // undistortor.undistortImage(currentFrame, undistorted);

    //convert to gray level only
    cvCvtColor(cloned, grayFrame, CV_BGR2GRAY);

    //reduce noise
    cvSmooth( grayFrame, grayFrame, CV_GAUSSIAN, 3, 3 );
			
            
    for (int y=0; y<frameSz.height; ++y) {
        laserDotArr[y] = findLaserCenterByRow((unsigned char *)&(grayFrame->imageData[y*grayFrame->widthStep]), frameSz.width); // GRAY IMAGE
        //laserDotArr[y] = findLaserCenterByRow((unsigned char *)&(cloned->imageData[y*grayFrame->widthStep]), frameSz.width); // COLORED IMAGE
    }
    // cout<<"size of height is"<<frameSz.height<<endl;

    for (int y=0; y<frameSz.height; ++y) {
        if (y % cloud_pt_row_delta == 0) {
            CloudPoint & currentpt = cloudpt_col[y/cloud_pt_row_delta];
            currentpt.row  = (y / cloud_pt_row_delta);
            currentpt.col= (currentAngle10 - opt_start_angle10)/opt_angle_stepping10;
            currentpt.height = cloud_pt_row_num;

            currentpt.X = currentpt.Y = currentpt.Z = 0;
        }

        //  if (y % 2) continue;
        //  if (laserDotArr[y] != -1) {
                //cvCircle(undistorted,cvPoint(laserDotArr[y],y),2,
				//y == frameSz.height/2?CV_RGB(255,0,0):CV_RGB(0,255,255));

                    char txtMsg[200];
                    if ( y == frameSz.height/2) {
                        sprintf(txtMsg,"x=%.3f.", laserDotArr[y]);
                        printf("current x=%.3f\n", laserDotArr[y]);
			printf("distance from middle frame is x=%.3f\n",(laserDotArr[y]-(frameSz.width/2)));
                        printf("-------------------------------------------------------------------------\n");
/*cvPutText(undistorted,txtMsg,cvPoint(laserDotArr[y],y),stdFont, 
cvScalar( 200,200,200));*/
                    }

                    
                    calcDistanceByPos(laserDotArr[y], y, frameSz.width,&result);
//printf("%.2f %.2f %.2f\n", result.distance,result.yaw * 180.0f/PI + currentAngle10/10, result.pitch* 180.0f/PI);

                    
                    float px, py ,pz ;
                    px = result.distance * cos(result.pitch) * sin(result.yaw  + currentAngle10*PI/10.0f/180.0f);
                    py = result.distance * cos(result.pitch) * cos(result.yaw  + currentAngle10*PI/10.0f/180.0f);
                    pz = result.distance * sin(-result.pitch);

                    if (fabs(px)>5000 || fabs(py)>5000 || fabs(pz)>1000) 
continue;
 
                    


                    if (y % cloud_pt_row_delta == 0)
                    {
                        CloudPoint & currentpt = cloudpt_col[y/cloud_pt_row_delta];


                        currentpt.X = px;
                        currentpt.Y = py;
                        currentpt.Z = pz;

                       // if (cloudpoint_file)
                            fprintf(dumpfile, "%.2f %.2f %.2f\n", px, py, pz );
                    }

                

            }            
            
            
            

           
        
		
	Mat imgMat(cloned);
	imwrite("picture.png", imgMat);
	Mat imgMat2(grayFrame);
	imwrite("picture2.png", imgMat2);
        delete [] cloudpt_col;
        //if (cloudpoint_file)
            fclose(dumpfile);
        delete [] laserDotArr;
		//delete [] cam_input;
		//delete [] dumpfile;
        cvReleaseImage(&grayFrame);
        cvReleaseImage(&undistorted);
		return 0;
	}


   /*  VideoCapture capture(0);
    capture.set(CV_CAP_PROP_FRAME_WIDTH,1920);
    capture.set(CV_CAP_PROP_FRAME_HEIGHT,1080);
    if(!capture.isOpened()){
            cout << "Failed to connect to the camera." << endl;
    }
    Mat frame, edges, grayFrame;
    capture >> frame;
    if(frame.empty()){
                cout << "Failed to capture an image" << endl;
                return -1;
    }
	cvtColor(frame, grayFrame, CV_BGR2GRAY);
	//reduce noise
    //cvSmooth( grayFrame, grayFrame, CV_GAUSSIAN, 3, 3 );
    cvtColor(frame, edges, CV_BGR2GRAY);
    Canny(edges, edges, 0, 30, 3);
    imwrite("gray.png", grayFrame);
    imwrite("capture.png", frame);
    return 0; */


float findLaserCenterByRow(unsigned char * row, size_t rowsz)
{
    static const unsigned char THRESHOLD_MIN_PWR = 25;
    static const unsigned char THRESHOLD_BLOB_DIFF = 10;
    static const int           THRESHOLD_ALLOWED_BLOB_SZ = 20;
    int centerPos = 0;
    unsigned char maxPwr = 0;
    int centerSize = 0;

    int currentPos = 0;
    while (currentPos<rowsz) {
        if (maxPwr<row[currentPos]) {
            centerSize = 1;
            int centerPos_candidate = currentPos;
            unsigned char maxPwr_candidate = row[currentPos];
            maxPwr=maxPwr_candidate;
            centerPos = centerPos_candidate;
        }
        else 
        {
            ++currentPos;
        }
    }

    if (maxPwr < THRESHOLD_MIN_PWR) return -1;

    float logicPwr = 0.0f, totalPwr=0.0f;

    for ( currentPos = centerPos-10; currentPos<=centerPos+10;currentPos++)
    {
        float currentPwr;
        if (currentPos>=0 && currentPos<rowsz){
           currentPwr = row[currentPos];
        }else{
           currentPwr = 0.0f;
        }
        logicPwr+=currentPwr;
        totalPwr+=currentPwr*currentPos;
    }

    return totalPwr/logicPwr;
}

void calcDistanceByPos( float x, int y, int img_width, MeasureResult *result)
{
	const double offset = -0.03460372108;	// Offset Constant
	const double gain = 0.00157772;
	float pixels_from_center = x - (img_width/2);
	
	cout << " X: " << x << " Y: " << y;
    
    double LASER_OFFSET = 0.03925299484;

	// Calculate range in cm based on bright pixel location, and setup specific constants
	double range = 6.1 / tan(pixels_from_center * gain + offset);
    
    int CENTER_Y = 239;
    if(y != CENTER_Y) {
        double NEW_Y = static_cast<double>(y);
        NEW_Y = abs(NEW_Y - CENTER_Y);
        NEW_Y *= 0.02645833333333;
        double theta = asin(NEW_Y/range);
        cout << " NEW_Y: " << NEW_Y << " THETA: " << theta << " TEST_RANGE: " << range;
        range = NEW_Y / tan(theta);
    }
    
	cout << " PFC: " << pixels_from_center << " RANGE: [" << range << "]" << endl;
    
/*
       dist = a/(b-c*x)+d
*/
    /*const float a = 698.1;
    const float b = 4.354;
    const float c = 0.006912;
    const float d = -40.88;
    
    const float baseline = 100.0;

    const float laser_angle = 1.486407302;
    const float rotation_r  = 49.2;
    const float focal = a/baseline;

    float center_distance = a/(b-c*x);

    float pitch_angle = atan(((y - img_width/2)*c)/(focal));
    float pitch_distance = center_distance/cos(pitch_angle);
    
    float laser_to_dist_pt = center_distance*tan(PI/2 - laser_angle);
    float laser_to_current_pt = sqrt(pitch_distance*pitch_distance + laser_to_dist_pt*laser_to_dist_pt);
    float laser_to_center_pt  = sqrt(center_distance*center_distance + laser_to_dist_pt*laser_to_dist_pt);


    float real_center_distance = sqrt( (laser_to_dist_pt-rotation_r)*(laser_to_dist_pt-rotation_r) +center_distance*center_distance);
    float yaw_angle = PI/2 - acos((rotation_r*rotation_r + real_center_distance*real_center_distance - 
laser_to_center_pt*laser_to_center_pt)/2.0f/rotation_r/real_center_distance);
 

    float real_distance = sqrt((laser_to_dist_pt-rotation_r)*(laser_to_dist_pt-rotation_r) +pitch_distance*pitch_distance);

    result->distance = real_distance;
    result->yaw = yaw_angle;
    result->pitch = pitch_angle -18.0*PI/180.0f;
    
    cout << " DISTANCE: [" << result->distance << "] YAW: [" << result->yaw << "] PITCH: [" << result->pitch << "]" << endl;*/
}
