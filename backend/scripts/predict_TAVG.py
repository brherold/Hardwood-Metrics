import numpy as np
import joblib

#FOR TEAM AVG BPM 
#Outputs OBPM, DBPM, BPM of player given stats (not per 100)


    


#off_values = [Poss,Pts,FGA,FTA,Off,AST,TO,FD]
#def_values = [OPoss,OPTS,OFGA,OFTA,DReb,STL,PF]

def predict_bpm_tavg(pos, off_values, def_values):
    # Load models based on position
    scaler_off = joblib.load(f"backend/BPM_Model_TAVG/scaler_off_{pos}.pkl")
    pca_off = joblib.load(f"backend/BPM_Model_TAVG/pca_off_{pos}.pkl")
    model_off = joblib.load(f"backend/BPM_Model_TAVG/model_off_{pos}.pkl")

    scaler_def = joblib.load(f"backend/BPM_Model_TAVG/scaler_def_{pos}.pkl")
    pca_def = joblib.load(f"backend/BPM_Model_TAVG/pca_def_{pos}.pkl")
    model_def = joblib.load(f"backend/BPM_Model_TAVG/model_def_{pos}.pkl")

    # Load y_off_pred and y_def_pred from training (assumed to be stored separately)
    y_off_pred = joblib.load(f"backend/BPM_Model_TAVG/y_off_pred_{pos}.pkl")  
    y_def_pred = joblib.load(f"backend/BPM_Model_TAVG/y_def_pred_{pos}.pkl")  
    
    #off_values = [Poss,Pts,FGA,FTA,Off,AST,TO,FD]
    #def_values = [OPoss,OPTS,OFGA,OFTA,DReb,STL,PF]


    off_per100 = [] #[Pts,Off,AST,TO,FD,TS%]
    def_per100 = [] #[OPTS,DReb,STL,PF,OTS%]

    #Fixes times when players play "0" minutes (essentially 1 possession)
    if off_values[0] == 0:
        off_values[0] = 1 
    if def_values[0] == 0:
        def_values[0] = 1

    #Calculates Per 100 for each non % stat
    for index, value in enumerate(off_values):
        if index not in [0,2,3]:
            off_per100.append(100 * (value / off_values[0]))
    
    #Calculates TS%
    if off_values[2] == 0 and off_values[3] == 0:
        off_per100.append(0)
    else:
        off_per100.append(off_values[1]/ (2 * (off_values[2] + .44 * off_values[3])))
    
    #Calculates Per 100 for each non % stat
    for index, value in enumerate(def_values):
        if index not in [0,2,3]:
            def_per100.append(100 * (value / def_values[0]))
    
    #Calculates TS%
    if def_values[2] == 0:
        def_per100.append(0)
    else:
        def_per100.append(def_values[1]/ (2 * (def_values[2] + .44 * def_values[3])))


    print(off_per100)
    print(def_per100)

    # Process offensive input
    off_val_np = np.array(off_per100).reshape(1, -1)
    off_input_scaled = scaler_off.transform(off_val_np)
    off_input_pca = pca_off.transform(off_input_scaled)
    obpm = model_off.predict(off_input_pca)[0]

    # Process defensive input
    def_val_np = np.array(def_per100).reshape(1, -1)
    def_input_scaled = scaler_def.transform(def_val_np)
    def_input_pca = pca_def.transform(def_input_scaled)
    dbpm = model_def.predict(def_input_pca)[0]

    # Compute mean and standard deviation from training predictions
    y_off_mean = np.mean(y_off_pred)
    y_off_std = np.std(y_off_pred)

    y_def_mean = np.mean(y_def_pred)
    y_def_std = np.std(y_def_pred)

    # Scaling the results
    target_mean, target_std = 0, 5  # Target scaling range

    obpm_scaled = ((obpm - y_off_mean) / y_off_std) * target_std + target_mean if y_off_std != 0 else target_mean
    dbpm_scaled = ((dbpm - y_def_mean) / y_def_std) * target_std + target_mean if y_def_std != 0 else target_mean
    bpm = obpm_scaled + dbpm_scaled

    return float(round(obpm_scaled, 1)), float(round(dbpm_scaled, 1)), float(round(bpm, 1))

'''
# Example usage
pos = "team"

#off_values = [Poss,Pts,FGA,FTA,Off,AST,TO,FD]
off_values = [79.491,84.232,69.566,16.667,11.165,14.267,13.766,15.168]

#def_values = [OPoss,OPTS,OFGA,OFTA,DReb,STL,PF]
def_values = [78.746,78.368,60.766,17.833,26.635,9.467,15.433]

print(predict_bpm_tavg(pos, off_values, def_values))
'''


