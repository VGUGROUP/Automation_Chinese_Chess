#include "Piece.h"
#include <fstream>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include "rapidcsv.h"


int paddTop = 10;
int paddLeft = 560;

cv::Mat importPic()                     //Accessing the camera using  DirectShow driver
{    
    cv::VideoCapture camera(1 + cv::CAP_DSHOW);
    cv::waitKey(200);
    cv::Mat image;

    camera.set(cv::CAP_PROP_FRAME_HEIGHT, 1080);
    camera.set(cv::CAP_PROP_FRAME_WIDTH, 1920);
    camera >> image;

    cv::Mat returnImg;
    returnImg = image(cv::Rect(paddLeft,paddTop,image.cols - paddLeft, image.rows - paddTop));

    cv::imwrite("source.png",returnImg);    
    return returnImg;
}


//Variables and functions for Hough Circle Transformation

const int dp = 127;
const int minDist = 20;
const int CannyEdgeDetect = 45;
const int CircleCenterDetect = 100;
const int minRad = 25;
const int maxRad = 70;

std::vector<cv::Vec3f> HoughTrans(cv::Mat boardMat)
{
    std::vector<cv::Vec3f> circles;
    cv::Mat grayMat;
    cv::Mat copyMat = boardMat.clone();
    cv::cvtColor(boardMat,grayMat,cv::COLOR_BGR2GRAY);

    cv::HoughCircles(grayMat,circles,cv::HOUGH_GRADIENT, (double) dp/100, (double)boardMat.rows/minDist,CannyEdgeDetect,CircleCenterDetect,minRad,maxRad );

    for( size_t i = 0; i < circles.size(); i++ )
    {
        cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
        int radius = cvRound(circles[i][2]);
        // circle center
        circle( copyMat, center, 3, cv::Scalar(0,255,0), -1, 8, 0 );
        // circle outline
        circle( copyMat, center, radius, cv::Scalar(0,0,255), 3, 8, 0 );
    }


    return circles;
}


//Variables and functions for HSV Filter

const int GreenLowH = 100;
const int GreenLowS = 0;
const int GreenLowV = 0;
const int GreenHighH = 165;
const int GreenHighS = 255;
const int GreenHighV = 255;


const int RedLowH = 140;
const int RedLowS = 0;
const int RedLowV = 0;
const int RedHighH = 255;
const int RedHighS = 255;
const int RedHighV = 255;


std::pair<int,int> HSVFilter(cv::Mat boardMat)
{
    cv::Scalar greenLow = cv::Scalar(GreenLowH,GreenLowS,GreenLowV);
    cv::Scalar greenHigh = cv::Scalar(GreenHighH,GreenHighS,GreenHighV);

    cv::Scalar redLow = cv::Scalar(RedLowH,RedLowS,RedLowV);
    cv::Scalar redHigh = cv::Scalar(RedHighH,RedHighS,RedHighV);

    cv::Mat HSVMat;
    cv::cvtColor(boardMat,HSVMat,cv::COLOR_BGR2HSV_FULL);

    cv::Mat greenBoard, redBoard;
    cv::inRange(HSVMat,greenLow,greenHigh,greenBoard);
    cv::inRange(HSVMat,redLow,redHigh,redBoard);

    int greenCount = cv::countNonZero(greenBoard);
    int redCount = cv::countNonZero(redBoard);

    return std::make_pair(greenCount,redCount);

}



//Variables and functions for ORB Calculate and BFMatching

const int nFeatures = 1600;
const int scaleFactors = 126;
const int nLevels = 16;
const int edgeThreshold = 20;
const int firstLevel = 3;
const int WTA_K = 2;
const cv::ORB::ScoreType scoreType = cv::ORB::HARRIS_SCORE;
const int patchSize = 37;
const int fastThreshhold = 23;

const int ratioThresh = 70;

cv::Mat ORB_Calculate(cv::Mat baseData)     //Function for calculating descriptor
{
    std::vector<cv::KeyPoint> keypoint;
    cv::Mat descriptor;
    cv::cvtColor(baseData,baseData,cv::COLOR_BGR2GRAY);
    cv::Ptr<cv::ORB> detector = cv::ORB::create(nFeatures,(float) scaleFactors/100, nLevels,edgeThreshold,firstLevel,WTA_K,scoreType,patchSize,fastThreshhold);
    detector->detect(baseData,keypoint);
    detector->compute(baseData,keypoint,descriptor);


    return descriptor;
}

int BF_Match(cv::Mat descriptor1, cv::Mat descriptor2)  //Function for matching descriptor
{
    cv::Ptr<cv::DescriptorMatcher> matcher = cv::BFMatcher::create(cv::NORM_HAMMING, false);
    std::vector<std::vector<cv::DMatch>> matches;

    matcher->knnMatch(descriptor1,descriptor2,matches,2);

    float ratio_thresh = (float) ratioThresh/100;
    float distance = 0;
    std::vector<cv::DMatch> good_matches;
    for (size_t i = 1; i < matches.size(); i++)
    {
        if (matches[i].size() != 0)
        {
            float bestPoint = matches[i][0].distance;
            float secondPoint = matches[i][1].distance * ratio_thresh;
            // std::cout << i << "\n";
            if (bestPoint < secondPoint)
            {
                good_matches.push_back(matches[i][0]);
                distance = distance + matches[i][0].distance;

            }
        }
    }
    // cv::drawMatches(pieceMat,keypoints1,boardMat,keypoints2,good_matches,imgMatch,cv:: Scalar::all(-1),cv:: Scalar::all(-1),std::vector<char>(),cv::DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);
    // cv::imshow("Result",imgMatch);

    distance = distance / good_matches.size();

    return good_matches.size();
}


// Function to write into a file
void writePiece(std::string fileName, std::vector<Piece>& pieceArray)
{
    std::ofstream output;
    output.open(fileName, std::ofstream::out | std::ofstream::trunc);
    output << "Name" << ',' << "Pos" << '\n' ;
    for (auto piece: pieceArray)
    {
        output << piece.getName() << ',' << (char)34 << "(" << piece.getBoardPos().first << ',' << " " << piece.getBoardPos().second << ")" << (char)34 << '\n';
    }

    output.close();
}


std::vector < std::pair<int, int>> advisorPosGen()
{
    std::vector<std::pair<int, int>> output;

    output.push_back(std::make_pair(1, 6));
    output.push_back(std::make_pair(1, 4));
    output.push_back(std::make_pair(2, 5));
    output.push_back(std::make_pair(3, 6));
    output.push_back(std::make_pair(3, 6));

    return output;
}


bool comparePiece(std::vector<Piece> detectedPiece, std::vector<std::string> machinePiece)
{
	std::vector<std::string> compareName;


	for (std::string tempName : machinePiece)
	{
		if (std::find(compareName.begin(), compareName.end(), tempName) == compareName.end())
		{
			compareName.push_back(tempName);
		}
	}

	std::vector<int> detectedCount, machineCount;

	for (std::string tempName : compareName)
	{
		int tempDetectCount = 0;
		int tempMachineCount = 0;
		for (Piece tempPiece : detectedPiece)
		{

			if (tempPiece.getName() == tempName)
			{
				tempDetectCount++;
			}
		}

		for (std::string tempMachineName : machinePiece)
		{
			if (tempMachineName == tempName)
			{
				tempMachineCount++;
			}
		}

		if ((tempDetectCount < tempMachineCount - 1) | (tempDetectCount > tempMachineCount))
		{
			return false;
		}
	}

	return true;
}


int main(int argc, char* argv[]) {

	// cv::Mat boardMat = cv::imread("boardCap2.png",cv::IMREAD_COLOR);
	//cv::Mat boardMat = cv::imread("source.jpg", cv::IMREAD_COLOR);
	int previousCount = 0;
	if (argc == 1)
	{
		previousCount = 32;
	}
	else
	{
		previousCount = atoi(argv[1]);
	}

	std::vector<cv::Mat> redDesc, greenDesc;
	std::vector<Piece> redArray, greenArray;
	int runCount = 0;

	while (runCount < 10)
	{
		runCount++;
		
		cv::Mat boardMat = importPic();
		for (int i = 0; i < 7; i++)
		{
			cv::Mat tempMat;
			std::string redPath = "Data/1/" + std::to_string(i) + ".png";
			tempMat = cv::imread(redPath, cv::IMREAD_COLOR);
			redDesc.push_back(ORB_Calculate(tempMat));

			std::string greenPath = "Data/-1/" + std::to_string(i) + ".png";
			tempMat = cv::imread(greenPath, cv::IMREAD_COLOR);
			greenDesc.push_back(ORB_Calculate(tempMat));
		}


		
		std::vector<cv::Vec3f> circles = HoughTrans(boardMat);
		std::cout << "Circles counting : " << circles.size() << "\n";
		std::cout << "Argument parsing: " << previousCount << "\n";
		if ((circles.size() < previousCount - 1)|(circles.size()> previousCount))
		{
			continue;
		}


		cv::Mat tempBoardMat = boardMat.clone();
		int red = 0;
		int green = 0;
		cv::Mat piece;
		
		std::cout << "Cutting and recognizing piece \n";
		for (int i = 0; i < circles.size(); i++)
		{
			piece = boardMat(cv::Rect(circles[i][0] - 43, circles[i][1] - 43, 90, 90));	
			cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
			cv::Mat descriptor = ORB_Calculate(piece);
			std::pair <int, int> position = std::make_pair(center.x, center.y);
			std::pair<int, int>  value = HSVFilter(piece);
			if (value.first > value.second)
			{
				//This is green Piece
				// std::string path = "Test/Green/" + std::to_string(green) + ".png";
				// cv::imwrite(path,piece);
				// green++;
				int bestMatch = 0;
				int bestMatchNo = 0;
				for (int count = 0; count < 7; count++)
				{
					int result = BF_Match(descriptor, greenDesc[count]);
					if (bestMatch < result)
					{
						bestMatch = result;
						bestMatchNo = count;
					}


				}
				Piece tempPiece((int)bestMatchNo, -1, position);
				greenArray.push_back(tempPiece);
				std::string text = tempPiece.getName() + std::to_string(tempPiece.getBoardPos().first) + " " + std::to_string(tempPiece.getBoardPos().second);
				cv::putText(tempBoardMat, text, center, cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(255, 255, 255), 2);
			}
			else
			{
				//This is red Piece
				// std::string path = "Test/Red/" + std::to_string(red) + ".png";
				// cv::imwrite(path,piece);
				// red++;
				int bestMatch = 0;
				int bestMatchNo = 0;
				for (int count = 0; count < 7; count++)
				{
					int result = BF_Match(descriptor, redDesc[count]);

					if (bestMatch < result)
					{
						bestMatch = result;
						bestMatchNo = count;
					}

				}
				Piece tempPiece((int)bestMatchNo, 1, position);
				redArray.push_back(tempPiece);

				std::string text = tempPiece.getName() + std::to_string(tempPiece.getBoardPos().first) + " " + std::to_string(tempPiece.getBoardPos().second);
				cv::putText(tempBoardMat, text, center, cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(255, 255, 255), 2);
			}

		}

		
		cv::imwrite("result.png", tempBoardMat);

		std::cout << "Advisor check \n";
		int advisorCount = 0;
		for (Piece tempPiece : greenArray)
		{
			if (tempPiece.getType() == 4)
				advisorCount = advisorCount + 1;
		}
		int pieceNum = 0;
		while ((advisorCount < 2) && (pieceNum < greenArray.size()))
		{
			std::vector<std::pair<int, int>> adviPos = advisorPosGen();
			for (std::pair<int, int> pos : adviPos)
			{
				if ((greenArray[pieceNum].getType() != 4) & (greenArray[pieceNum].getBoardPos() == pos))
					/*&(greenArray[pieceNum].getType() != 5)*/
				{
					greenArray[pieceNum].setType(4);
					break;
				}
			}
			pieceNum++;
		}


		std::cout << "Immport CSV \n";
		rapidcsv::Document mGreenFile("m_GreenPiece.csv", rapidcsv::LabelParams(0, -1));
		rapidcsv::Document mRedFile("m_RedPiece.csv", rapidcsv::LabelParams(0, -1));


		std::cout << "Comparing pieces \n";
		std::vector<std::string> mGreenArray = mGreenFile.GetColumn<std::string>(0);
		std::vector<std::string> mRedArray = mRedFile.GetColumn<std::string>(0);

		if ((comparePiece(greenArray, mGreenArray) == false) | (comparePiece(redArray, mRedArray) == false))
		{
			std::cout << "Compare failed - Piece list mismatched";
			continue;
		}
		
		

		writePiece("RedPiece.csv", redArray);
		writePiece("GreenPiece.csv", greenArray);
		cv::namedWindow("image", cv::WINDOW_AUTOSIZE);
		cv::imshow("image", tempBoardMat);

		cv::waitKey();
		break;
	}

	if (runCount == 10)
	{
		std::cout << "Exceed running instances \n";
		writePiece("RedPiece.csv", redArray);
		writePiece("GreenPiece.csv", greenArray);
		cv::waitKey();
	}
}




