#include <iostream>
#include <random>
#include <string>

using namespace std;

// constants
const int maxIndividuals = 35000;
const int maxReactions = 2;

struct CFG{
    // config
    int randSeed = 53;
    float r = 1;
    float K = 30;
    int N0 = 10;
    float maxTime = 30;
};

struct iState{
    // Defaults to dead, without id
    int id;
    bool isAlive = false;
};

// propensity functions
float birthRate(struct CFG cfg, struct iState s, int N){
    if(s.isAlive){
        return cfg.r;
    }else{
        return 0;
    }
}
float deathRate(struct CFG cfg, struct iState s, int N){
    if(s.isAlive){
        return cfg.r*N/cfg.K;
    }else{
        return 0;
    }
}

struct Reaction{
    int indivId;
    char type;
    float propensity;
};

// global state - this is continuously changed
struct globalState{

    int N;
    iState populationArray[maxIndividuals];

    Reaction reactionArray[maxIndividuals*maxReactions];
    float propensityArray[maxIndividuals*maxReactions];
    float totPropensity;
    float minNonZeroPropensity;

    float t = 0;
    float dt;

    int reactionIdx;
    char reactionType;

    bool isTerminalState = false;
    string terminalLog;

};

void initGlobalState(struct globalState& gState, struct CFG cfg){

    // Init population array and populations number
    for(int i=0; i<cfg.N0; i++){
        gState.populationArray[i].id = i;
        gState.populationArray[i].isAlive = true;
    }
    gState.N = cfg.N0;

    // Init reaction array, propensity array and total propensity
    float totProp = 0;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float bRate = birthRate(cfg, s, cfg.N0);
        gState.reactionArray[maxReactions*i + 0].indivId = i;
        gState.reactionArray[maxReactions*i + 0].type = '+';
        gState.reactionArray[maxReactions*i + 0].propensity = bRate;
        totProp += bRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float dRate = deathRate(cfg, s, cfg.N0);
        gState.reactionArray[maxReactions*i + 1].indivId = i;
        gState.reactionArray[maxReactions*i + 1].type = '-';
        gState.reactionArray[maxReactions*i + 1].propensity = dRate;
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

    }
    gState.totPropensity = totProp;

}

void printGlobalState(struct globalState gState){

    if(!gState.isTerminalState){

            //cout << "t: " << gState.t << " N: " << gState.N << '\n';

            string populationAliveLog = "";
            int aliveCount = 0;
            for(int i=0; i<maxIndividuals; i++){
                if(gState.populationArray[i].isAlive){
                    populationAliveLog += '*';
                    aliveCount += 1;
                }else{
                    populationAliveLog += '_';
                }
                if(aliveCount==gState.N){
                    break;
                }
            }
            cout << gState.t << " " << populationAliveLog << '\n';

        /*
            string reactionTypeLog = "";
            string reactionPropLog = "";
            aliveCount = 0;
            for(int i=0; i<maxIndividuals; i++){
                if(gState.populationArray[i].isAlive){
                    reactionTypeLog += gState.reactionArray[maxReactions*i +0].type;
                    reactionTypeLog += gState.reactionArray[maxReactions*i +1].type;
                    aliveCount += 1;
                }else{
                    reactionTypeLog += "__";
                }
                reactionPropLog += to_string(gState.propensityArray[maxReactions*i +0])+" ";
                reactionPropLog += to_string(gState.propensityArray[maxReactions*i +1])+" ";
                if(aliveCount==gState.N){
                    break;
                }
            }
            cout << reactionTypeLog << '\n';
            cout << reactionPropLog << '\n';
        */
    }else{
        cout << gState.terminalLog;
    }

}

void printCsvLine(struct globalState gState){
    cout << gState.t <<','<<gState.N<<'\n';
}

void updatePropensities(struct globalState& gState, struct CFG& cfg){

    float totProp = 0;
    int aliveCount = 0;
    float minNonZeroPropensity = gState.totPropensity;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float bRate = birthRate(cfg, s, gState.N);
        totProp += bRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float dRate = deathRate(cfg, s, gState.N);
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

        // Look for minimum propensity interval
        if(bRate!=0 and bRate<minNonZeroPropensity);
            minNonZeroPropensity = bRate;
        if(dRate!=0 and dRate<minNonZeroPropensity);
            minNonZeroPropensity = dRate;

        if(s.isAlive){
            aliveCount += 1;
            if(aliveCount==gState.N){
                break;
            }
        }

    }
    gState.totPropensity = totProp;
    gState.minNonZeroPropensity = minNonZeroPropensity;

}

void selectTime(struct globalState& gState, float r1){

    float meanTime = 1/gState.totPropensity;
    float dt = meanTime*log(1/r1);
    gState.dt = dt;
    gState.t += dt;

}

void selectReaction(struct globalState& gState, float r2){

    int reactionIdx = 0;
    float randValue = gState.totPropensity*r2;
    float cumulativeProp = gState.propensityArray[reactionIdx];
    while(randValue > cumulativeProp){
        reactionIdx += 1;
        cumulativeProp = gState.propensityArray[reactionIdx];
    }
    gState.reactionIdx = reactionIdx;
    gState.reactionType = gState.reactionArray[reactionIdx].type;

}

void birth(struct globalState& gState){

    for(int i=0; i<maxIndividuals; i++){
        if( ! gState.populationArray[i].isAlive ){
            gState.populationArray[i].isAlive = true;
            gState.N += 1;
            break;
        }
    }
}

void death(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;
    gState.populationArray[indivId].isAlive = false;
    gState.N += -1;

}

void applyReaction(struct globalState& gState){

    if(gState.reactionType=='+'){
        birth(gState);
    }else if(gState.reactionType=='-'){
        death(gState);
    }

}

void checkTerminalState(struct globalState& gState, struct CFG& cfg){

    if(gState.t > cfg.maxTime){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max time\n";
    }else if(gState.N==1 && gState.reactionType=='-'){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: extinction\n";
    }else if(gState.N==maxIndividuals-1 && gState.reactionType=='+'){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max population\n";
    }

}

void step(struct globalState& gState, struct CFG& cfg){



}
