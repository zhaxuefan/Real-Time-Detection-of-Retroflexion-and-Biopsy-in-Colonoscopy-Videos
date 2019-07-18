feature = zeros(768,21);
for t = 1:768
    %feature one
    if length(area{t}) > 1
        [feature(t,1),loc] = max(area{t});
        feature(t,1) = area{t}(loc);
        feature(t,2) = perimeter{t}(loc);
        feature(t,3) = rect_width{t}(loc);
        feature(t,4) = PPD{t}(loc);
        feature(t,5) = roundness{t}(loc);
        feature(t,6) = convexity{t}(loc);
        feature(t,7) = curl{t}(loc);
        feature(t,8) = eccentricity_score{t}(loc);
        feature(t,9) = aspect_ratio_score{t}(loc);
        feature(t,10) = extent_score{t}(loc);
        feature(t,11) = solidity_score{t}(loc);
        feature(t,12) = kcurve{t}(loc);
        feature(t,13) = areaRGB_score{t}(loc,1);
        feature(t,14) = areaRGB_score{t}(loc,2);
        feature(t,15) = areaRGB_score{t}(loc,3);
        feature(t,16) = areaHSV_score{t}(loc,1);
        feature(t,17) = areaHSV_score{t}(loc,2);
        feature(t,18) = areaHSV_score{t}(loc,3);
        feature(t,19) = areaLAB_score{t}(loc,1);
        feature(t,20) = areaLAB_score{t}(loc,2);
        feature(t,21) = areaLAB_score{t}(loc,3);
    else
        feature(t,1) = area{t};
        feature(t,2) = perimeter{t};
        feature(t,3) = rect_width{t};
        feature(t,4) = PPD{t};
        feature(t,5) = roundness{t};
        feature(t,6) = convexity{t};
        feature(t,7) = curl{t};
        feature(t,8) = eccentricity_score{t};
        feature(t,9) = aspect_ratio_score{t};
        feature(t,10) = extent_score{t};
        feature(t,11) = solidity_score{t};
        feature(t,12) = kcurve{t};
        if length(areaRGB_score{t}) == 0
            feature(t,13) = 0;
            feature(t,14) = 0;
            feature(t,15) = 0;
            feature(t,16) = 0;
            feature(t,17) = 0;
            feature(t,18) = 0;
            feature(t,19) = 0;
            feature(t,20) = 0;
            feature(t,21) = 0;
        else
            feature(t,13) = areaRGB_score{t}(:,1);
            feature(t,14) = areaRGB_score{t}(:,2);
            feature(t,15) = areaRGB_score{t}(:,3);
            feature(t,16) = areaHSV_score{t}(:,1);
            feature(t,17) = areaHSV_score{t}(:,2);
            feature(t,18) = areaHSV_score{t}(:,3);
            feature(t,19) = areaLAB_score{t}(:,1);
            feature(t,20) = areaLAB_score{t}(:,2);
            feature(t,21) = areaLAB_score{t}(:,3);
        end
    end
end
        
     
        
        
       
        
        
        
        
        