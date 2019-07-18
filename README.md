# Real-Time-Detection-of-Retroflexion-and-Biopsy-in-Colonoscopy-Videos

The whole system design is as flowchart below:
![image](https://github.com/zhaxuefan/image/blob/master/7186.png)


Materials and Methods: The work is divided into three parts, feature extraction, optimization and comparison.
●	Region-based feature descriptor
Color mask based on HSV color space and adaptive threshold canny(auto-canny) edge detection is used to segment potential area. After getting masks, label 8-connectivity bounding mask and filled all contours with convex hull shape. Based on this, shape descriptors are made to judge those aligned candidate areas. 15 features involved in judging candidate areas including rectangularity, compactness, curvature and etc.
●	Optimization based on Genetic algorithm(GA)
Taken different influence on detection across features into account, it has been tested that threshold manually selected can’t fit for all videos. GA is a global optimal solution searching algorithm to minimize tradeoff between input feature and judgement[2]. Data normalization, feature encoding as chromosome design and weighted majority voter as fitness function design is used in GA optimization in paper.
●	Comparison with machine learning and deep learning model
SVM is also good classification tool in soft margin classification problem, constructed feature matrix is also put into SVM to compare classification result with GA. In order to make model more explainable, one of best image classification model in deep learning, ResNet50 is compared. Using raw image data as input of deep neural network. 


![image](https://github.com/zhaxuefan/image/blob/master/7187.png)
