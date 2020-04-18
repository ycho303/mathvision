#include "polygon_demo.hpp"
#include "opencv2/imgproc.hpp"
#include <iostream>
#include <cmath>
#include "eigen/Eigen/Dense"
#include "eigen/Eigen/Jacobi"
#define _USE_MATH_DEFINES
#include <math.h>

using Eigen::MatrixXd;

using namespace std;
using namespace cv;

PolygonDemo::PolygonDemo()
{
    m_data_ready = false;
}

PolygonDemo::~PolygonDemo()
{
}

void PolygonDemo::refreshWindow()
{
    Mat frame = Mat::zeros(480, 640, CV_8UC3);
    if (!m_data_ready)
        putText(frame, "Input data points (double click: finish)", Point(10, 470), FONT_HERSHEY_SIMPLEX, .5, Scalar(0, 148, 0), 1);
        string gui_str = "false";
        if (m_param.ransac && m_param.fit_circle) gui_str = "true";
        putText(frame, "Double right click for RANSAC: " + gui_str, Point(10, 20), FONT_HERSHEY_SIMPLEX, .5, Scalar(0, 148, 0), 1);

    drawPolygon(frame, m_data_pts, m_data_ready);
    if (m_data_ready)
    {
        // fit circle
        if (m_param.fit_circle)
        {
            Point2d center;
            double radius = 0;
            bool ok = fitCircle(m_data_pts, center, radius);

            if (m_param.ransac) {
                ok = compute_circle_ransac(m_data_pts, center, radius);
            }

            if (ok)
            {
                circle(frame, center, (int)(radius + 0.5), Scalar(0, 255, 0), 1);
                circle(frame, center, 2, Scalar(0, 255, 0), cv::FILLED);
            }
        }

        // fit ellipse
        if (m_param.fit_ellipse)
        {
            Size axes;
            Point2d center;
            double angle = 0;
            bool ok = fitEllipse(m_data_pts, center, axes, angle);

            if (ok)
            {
                ellipse(frame, center, axes, angle, 0, 360, Scalar(0, 255, 0), 1);
            }
        }
    }

    imshow("PolygonDemo", frame);
}

// return the area of polygon
int PolygonDemo::polyArea(const std::vector<cv::Point>& vtx)
{
    double area = 0;
    for (int i = 0; i < vtx.size(); i++)
    {
        cout << "\n (" << vtx[i].x << ", " <<  vtx[i].y << ")";
        int j = (i + 1) % vtx.size();
        area += (vtx[i].x * vtx[j].y - vtx[j].x * vtx[i].y) * 0.5;
    }
    return abs(area);
}

// return true if pt is interior point
bool PolygonDemo::ptInPolygon(const std::vector<cv::Point>& vtx, Point pt)
{
    return false;
}

// return homography type: NORMAL, CONCAVE, TWIST, REFLECTION, CONCAVE_REFLECTION
int PolygonDemo::classifyHomography(const std::vector<cv::Point>& pts1, const std::vector<cv::Point>& pts2)
{
    if (pts1.size() != 4 || pts2.size() != 4) return -1;
    
    for (int j = 0; j < 4; j++)
    {
        int i = (j - 1) % pts1.size();
        int k = (j + 1) % pts1.size();

        Point pp1, pp2, qq1, qq2;
        pp1.x = pts1[j].x * pts1[i].x;
        pp1.y = pts1[j].y * pts1[i].y;

        pp2.x = pts1[j].x * pts1[k].x;
        pp2.y = pts1[j].y * pts1[k].y;

        qq1.x = pts2[j].x * pts2[i].x;
        qq1.y = pts2[j].y * pts2[i].y;
        qq2.x = pts2[j].x * pts2[k].x;
        qq2.y = pts2[j].y * pts2[k].y;

        cout << qq1;
    }

    return NORMAL;
}

// estimate a circle that best approximates the input points and return center and radius of the estimate circle
bool PolygonDemo::fitCircle(const std::vector<cv::Point>& pts, cv::Point2d& center, double& radius)
{
    int n = (int)pts.size();
    if (n < 3) return false;

    MatrixXd A(n, 3);
    MatrixXd b(n, 1);
    for (int i = 0; i < n; i++) {
        // A matrix
        for (int j = 0; j < 3; j++) {
            if (j == 0) A(i, j) = pts[i].x;
            else if (j == 1) A(i, j) = pts[i].y;
            else if (j == 2) A(i, j) = 1;
        }

        // b matrix
        b(i, 0) = -pow(pts[i].x, 2) - pow(pts[i].y, 2);
    }
    // Pseudo matrix
    MatrixXd A_t = A.transpose();
    MatrixXd x;

    if ((A_t * A).determinant() != 0) {
        MatrixXd A_pinv = (A_t * A).inverse() * A_t;
        // Get a, b and c
        x = A_pinv * b;
    }
    else if ((A * A_t).determinant() != 0) {
        MatrixXd A_pinv = A_t * (A * A_t).inverse();
        // Get a, b and c
        x = b * A_pinv;
    }

    // Center and radius
    center.x = -1 * (x(0, 0) / 2);
    center.y = -1 * (x(1, 0) / 2);
    radius = sqrt(pow(x(0, 0), 2)/4 + (pow(x(1, 0), 2) / 4 - x(2, 0)));
    return true;
}


bool PolygonDemo::compute_circle_ransac(const std::vector<cv::Point>& pts, cv::Point2d& center, double& radius) {
    int n = (int)pts.size();
    if (n < 4) return false;

    int sample_iteration = 1000;
    int count_fit = 0;
    int best_fit = 0;
    int sample = 4;
    int r_margin = 100;
    double best_radius = radius;
    std::vector<cv::Point> m_sample_pts;
    
    for (int m = 0; m < sample_iteration; m++) {
        // sample data
        m_sample_pts.clear();
        int* sample_index = sampler(sample, n);
        for (int i = 0; i < sample; i++) {
            m_sample_pts.push_back(Point(pts[sample_index[i]].x, pts[sample_index[i]].y));
        }
        
        // create circle and evaluate
        bool ok = fitCircle(m_sample_pts, center, radius);
        if (ok) {
            count_fit = 0;
            for (int i = 0; i < n; i++) {
                double dist = pow(pts[i].x - center.x, 2) + pow(pts[i].y - center.y, 2);

                if (dist <= pow(radius, 2)) {
                    count_fit += 1;
                }
            }
            if ((count_fit > best_fit) && (radius < best_radius + r_margin)) {
                best_fit = count_fit;
                best_radius = radius;
            }
        }
    }
    return true;
}

int* PolygonDemo::sampler(int sample_size, int population_size) {
    int* sampled = new int[sample_size];
    vector<int> check;
    for (int i = 0; i < population_size; i++) {
        check.push_back(0);
    }
    int num, count = 0;
    
    while (count < sample_size) {
        num = rand() % population_size;

        if (check[num] == 0) {
            check[num] = 1;
            sampled[count] = num;
            count++;
        }
    }
    return sampled;
}

// estimate a ellipse that best approximates the input points and return center and radius of the estimate ellipse
bool PolygonDemo::fitEllipse(const std::vector<cv::Point>& pts, cv::Point2d& center, cv::Size& axes, double& angle)
{
    int n = (int)pts.size();
    if (n < 4) return false;

    Mat A = Mat::zeros(n, 6, CV_64F);
    for (int i = 0; i < n; i++) {
        // A matrix
        for (int j = 0; j < 6; j++) {
            if (j == 0) A.at<double>(i, j) = pow(pts[i].x, 2);
            else if (j == 1) A.at<double>(i, j) = pts[i].x * pts[i].y;
            else if (j == 2) A.at<double>(i, j) = pow(pts[i].y, 2);
            else if (j == 3) A.at<double>(i, j) = pts[i].x;
            else if (j == 4) A.at<double>(i, j) = pts[i].y;
            else if (j == 5) A.at<double>(i, j) = 1;
        }
    }

    double a, b, c, d, e, f;
    Mat U, S, V, x;
    SVD::compute(A, U, S, V, SVD::FULL_UV);
    x = V.t(); // not exactly x
    int last_idx = x.size[1] - 1;
    a = x.at<double>(0, last_idx);
    b = x.at<double>(1, last_idx);
    c = x.at<double>(2, last_idx);
    d = x.at<double>(3, last_idx);
    e = x.at<double>(4, last_idx);
    f = x.at<double>(5, last_idx);
    
    double semi_axis1 = -sqrt(2 * (a * pow(e, 2) + c * pow(d, 2) - b * d * e + (pow(b, 2) - 4 * a * c) * f) * ((a + c) + sqrt(pow(a - c, 2) + pow(b, 2)))) / (pow(b, 2) - 4 * a * c);
    double semi_axis2 = -sqrt(2 * (a * pow(e, 2) + c * pow(d, 2) - b * d * e + (pow(b, 2) - 4 * a * c) * f) * ((a + c) - sqrt(pow(a - c, 2) + pow(b, 2)))) / (pow(b, 2) - 4 * a * c);
    axes = Size(max(semi_axis1, semi_axis2) , min(semi_axis1, semi_axis2));
    center.x = (b * e - 2 * c * d) / (4 * a * c - pow(b, 2));
    center.y = (b * d - 2 * a * e) / (4 * a * c - pow(b, 2));

    angle = 0.5 * atan2(b, a - c);
    if (semi_axis1 > semi_axis2) angle += M_PI_2;
    angle *= 180 / M_PI;

    return true;
}

bool PolygonDemo::compute_ellipse_ransac(const std::vector<cv::Point>& pts, cv::Point2d& center, cv::Size& axes, double& angle) {
    int n = (int)pts.size();
    if (n < 4) return false;

    int sample_iteration = 20;
    int count_fit = 0;
    int best_fit = 0;
    int sample = 5;
    std::vector<cv::Point> m_sample_pts;
    Point2d best_center = center;
    Size best_axes = axes;
    double best_angle = angle;

    for (int m = 0; m < sample_iteration; m++) {
        // sample data
        m_sample_pts.clear();
        int* sample_index = sampler(sample, n);
        for (int i = 0; i < sample; i++) {
            m_sample_pts.push_back(Point(pts[sample_index[i]].x, pts[sample_index[i]].y));
        }

        // create circle and evaluate
        bool ok = fitEllipse(m_data_pts, center, axes, angle);
        if (axes.width < 0) continue;
        if (ok) {
            count_fit = 0;
            for (int i = 0; i < n; i++) {
                if ((pow((pts[i].x - center.x), 2) / pow(axes.width, 2)) + (pow((pts[i].y - center.y), 2) / pow(axes.height, 2)) <= 1) {
                    count_fit += 1;
                }
            }
            if (count_fit > best_fit && (best_axes.width < axes.width || best_axes.height < axes.height)) {
                best_fit = count_fit;
                best_center.x = center.x;
                best_center.y = center.y;
                best_axes = Size(axes.width, axes.height);
                best_angle = angle;
            }
        }
    }

    center.x = best_center.x;
    center.y = best_center.y;
    axes = Size(best_axes.width, best_axes.height);
    angle = best_angle;
    return true;
}

void PolygonDemo::drawPolygon(Mat& frame, const std::vector<cv::Point>& vtx, bool closed)
{
    int i = 0;
    for (i = 0; i < (int)m_data_pts.size(); i++)
    {
        circle(frame, m_data_pts[i], 2, Scalar(255, 255, 255), cv::FILLED);
    }
}

void PolygonDemo::handleMouseEvent(int evt, int x, int y, int flags)
{
    if (evt == cv::EVENT_LBUTTONDOWN)
    {
        if (!m_data_ready)
        {
            m_data_pts.push_back(Point(x, y));
            refreshWindow();
        }
        else
        {
            m_test_pts.push_back(Point(x, y));
        }
        
    }
    else if (evt == cv::EVENT_LBUTTONUP)
    {
    }
    else if (evt == cv::EVENT_LBUTTONDBLCLK)
    {
        m_data_ready = true;
        refreshWindow();
    }
    else if (evt == cv::EVENT_RBUTTONDBLCLK)
    {
        if (m_param.ransac) m_param.ransac = false;
        else m_param.ransac = true;
        refreshWindow();
    }
    else if (evt == cv::EVENT_MOUSEMOVE)
    {
    }
    else if (evt == cv::EVENT_RBUTTONDOWN)
    {
        m_data_pts.clear();
        m_test_pts.clear();
        m_data_ready = false;
        refreshWindow();
    }
    else if (evt == cv::EVENT_RBUTTONUP)
    {
    }
    else if (evt == cv::EVENT_MBUTTONDOWN)
    {
    }
    else if (evt == cv::EVENT_MBUTTONUP)
    {
    }

    if (flags&cv::EVENT_FLAG_LBUTTON)
    {
    }
    if (flags&cv::EVENT_FLAG_RBUTTON)
    {
    }
    if (flags&cv::EVENT_FLAG_MBUTTON)
    {
    }
    if (flags&cv::EVENT_FLAG_CTRLKEY)
    {
    }
    if (flags&cv::EVENT_FLAG_SHIFTKEY)
    {
    }
    if (flags&cv::EVENT_FLAG_ALTKEY)
    {
    }
}
