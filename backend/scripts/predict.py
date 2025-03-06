import numpy as np
import joblib

#Outputs OBPM, DBPM, BPM of player given stats (not per 100)

#Includes converting stats to Per 100 (and getting TS% and eOfg%)
#Have the models folder and you dont it saves the models 
    
    #OeFG == TS when no free throws 

#off_values = [Poss,Pts,FGA,FTA,Off,AST,TO,FD]
#def_values = [OPoss,OPTS,OFGA,DReb,STL,PF]

def predict_bpm(pos, off_values, def_values):
    # Load models based on position
    scaler_off = joblib.load(f"backend/BPM_Model/scaler_off_{pos}.pkl")
    pca_off = joblib.load(f"backend/BPM_Model/pca_off_{pos}.pkl")
    model_off = joblib.load(f"backend/BPM_Model/model_off_{pos}.pkl")

    scaler_def = joblib.load(f"backend/BPM_Model/scaler_def_{pos}.pkl")
    pca_def = joblib.load(f"backend/BPM_Model/pca_def_{pos}.pkl")
    model_def = joblib.load(f"backend/BPM_Model/model_def_{pos}.pkl")

    # Load y_off_pred and y_def_pred from training 
    y_off_pred = joblib.load(f"backend/BPM_Model/y_off_pred_{pos}.pkl")  
    y_def_pred = joblib.load(f"backend/BPM_Model/y_def_pred_{pos}.pkl")  
    
    #off_values = [Poss,Pts,FGA,FTA,Off,AST,TO,FD]
    #def_values = [OPoss,OPTS,OFGA,DReb,STL,PF]



    off_per100 = [] #[Pts,Off,AST,TO,FD,TS%]
    def_per100 = [] #[OPTS,DReb,STL,PF,OeFG%]

    #Fixes times when players play "0" minutes (essentially 1 possession)
    if off_values[0] == 0:
        off_values[0] = 1 
    if def_values[0] == 0:
        def_values[0] = 1


    for index, value in enumerate(off_values):
        if index not in [0,2,3]:
            off_per100.append(100 * (value / off_values[0]))
    
    if off_values[2] == 0 and off_values[3] == 0:
        off_per100.append(0)
    else:
        off_per100.append(off_values[1]/ (2 * (off_values[2] + .44 * off_values[3])))
    
    for index, value in enumerate(def_values):
        if index not in [0,2]:
            def_per100.append(100 * (value / def_values[0]))
    
    if def_values[2] == 0:
        def_per100.append(0)
    else:
        def_per100.append(def_values[1]/ (2 * def_values[2]))



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
pos = "C"
off_values = [51.9,16,8,4,1,4,1,5]
def_values = [51.9,10,8,6,0,5]

print(predict_bpm(pos, off_values, def_values))
#'''


