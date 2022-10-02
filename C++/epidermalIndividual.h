#include <iostream>
#include <random>
#include <string>
#include <cmath>

using namespace std;

// constants
const int maxIndividuals = 35000;
const int maxReactions = 3;

struct CFG{
    // config
    int randSeed = 123546;
    float lambda = 30;
    float tau = 3;
    int S0 = 1;
    int G0 = 0;
    int N0 = 0;
    float maxTime = 1000;
};

struct iState{
    // Defaults to dead, without id
    int id;
    bool isAlive = false;
    float age = 0;
    char group;
};

// propensity functions
float sReaction(struct CFG cfg, struct iState s){

    float rate = 0;
    if(s.isAlive){
        if(s.group=='S'){
            rate = cfg.lambda;
        }
    }
    return rate;

}

float mu(float age){
    float d = 0.03;
    float m = 2.0;
    return (m*d)*pow((age*d), m-1);
}

float nReaction(struct CFG cfg, struct iState s){

    float rate = 0;
    if(s.isAlive){
        if(s.group=='N'){
            rate = mu(s.age);
        }
    }
    return rate;

}

float gReaction(struct CFG cfg, struct iState s){

        float rate = 0;
        if(s.isAlive){
            if(s.group=='G'){
                rate = exp(s.age - cfg.tau);
            }
        }
        return rate;

}

struct Reaction{
    int indivId;
    char type;
    float propensity;
};

// global state - this is continuously changed
struct globalState{

    int nS;
    int nG;
    int nN;
    iState populationArray[maxIndividuals];

    Reaction reactionArray[maxIndividuals*maxReactions];
    float propensityArray[maxIndividuals*maxReactions];
    float totPropensity;

    float t = 0;
    float dt;

    int reactionIdx;
    char reactionType;

    bool isTerminalState = false;
    string terminalLog;

};

void initGlobalState(struct globalState& gState, struct CFG cfg){

    // Init population array and populations number
    for(int i=0; i<cfg.S0; i++){
        gState.populationArray[i].id = i;
        gState.populationArray[i].isAlive = true;
        gState.populationArray[i].group='S';
        gState.populationArray[i].age = 0;
    }
    for(int i=0; i<cfg.G0; i++){
        gState.populationArray[cfg.S0+i].id = i;
        gState.populationArray[cfg.S0+i].isAlive = true;
        gState.populationArray[cfg.S0+i].group='G';
        gState.populationArray[cfg.S0+i].age = 0;
    }
    for(int i=0; i<cfg.N0; i++){
        gState.populationArray[cfg.S0+cfg.G0+i].id = i;
        gState.populationArray[cfg.S0+cfg.G0+i].isAlive = true;
        gState.populationArray[cfg.S0+cfg.G0+i].group='N';
        gState.populationArray[cfg.S0+cfg.G0+i].age = 0;
    }
    gState.nS = cfg.S0;
    gState.nG = cfg.G0;
    gState.nN = cfg.N0;

    // Init reaction array, propensity array and total propensity
    float totProp = 0;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float sRate = sReaction(cfg, s);
        gState.reactionArray[maxReactions*i + 0].indivId = i;
        gState.reactionArray[maxReactions*i + 0].type = 'S';
        gState.reactionArray[maxReactions*i + 0].propensity = sRate;
        totProp += sRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float nRate = nReaction(cfg, s);
        gState.reactionArray[maxReactions*i + 1].indivId = i;
        gState.reactionArray[maxReactions*i + 1].type = 'N';
        gState.reactionArray[maxReactions*i + 1].propensity = nRate;
        totProp += nRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

        float gRate = gReaction(cfg, s);
        gState.reactionArray[maxReactions*i + 2].indivId = i;
        gState.reactionArray[maxReactions*i + 2].type = 'G';
        gState.reactionArray[maxReactions*i + 2].propensity = gRate;
        totProp += gRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

    }
    gState.totPropensity = totProp;

}

void printGlobalState(struct globalState gState){

    if(!gState.isTerminalState){

//            cout << "t: " << gState.t << " nG: " << gState.nG << " nN: " << gState.nN << '\n';

            string populationAliveLog = "";
/*
            int aliveCount = 0;
            for(int i=0; i<maxIndividuals; i++){
                if(gState.populationArray[i].isAlive){
                    if(gState.populationArray[i].group == 'G'){
                        populationAliveLog += 'G';
                    }else{
                        populationAliveLog += 'N';
                    }
                    aliveCount += 1;
                }else{
                    populationAliveLog += '_';
                }
                if(aliveCount==(gState.nS+gState.nG+gState.nN)){
                    break;
                }
            }
*/
            for(int i=0; i<gState.nS; i++){
                populationAliveLog += 'S';
            }
            for(int i=0; i<gState.nG; i++){
                populationAliveLog += 'G';
            }
            for(int i=0; i<gState.nN; i++){
                populationAliveLog += 'N';
            }

            cout << gState.t << " " << populationAliveLog << '\n';
    }else{
        cout << gState.terminalLog;
    }

}

void printCsvLine(struct globalState gState){
    cout << gState.t <<','<< gState.nS <<','<< gState.nG <<','<< gState.nN <<'\n';
}

void updatePropensities(struct globalState& gState, struct CFG& cfg){

    float totProp = 0;
    int aliveCount = 0;
    int totIndividuals = gState.nS + gState.nG + gState.nN;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float sRate = sReaction(cfg, s);
        totProp += sRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float dRate = nReaction(cfg, s);
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

        float gRate = gReaction(cfg, s);
        totProp += gRate;
        gState.propensityArray[maxReactions*i + 2] = totProp;

        if(s.isAlive){
            aliveCount += 1;
            if(aliveCount==totIndividuals){
                break;
            }
        }

    }
    gState.totPropensity = totProp;

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

void stemIntoG(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;
    gState.populationArray[indivId].group = 'G';
    gState.nS += -1;
    gState.nG += 1;

}

void birth(struct globalState& gState, char group){

    for(int i=0; i<maxIndividuals; i++){
        if( ! gState.populationArray[i].isAlive ){
            gState.populationArray[i].isAlive = true;
            gState.populationArray[i].group = group;
            gState.populationArray[i].age = 0;
            break;
        }
    }
}

void death(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;
    gState.populationArray[indivId].isAlive = false;
    gState.nN += -1;

}

void gSplit(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;

    gState.populationArray[indivId].group = 'N';
    gState.populationArray[indivId].age = 0;
    gState.nG += -1;
    gState.nN += 1;
    birth(gState, 'S');
    gState.nS += 1;

}

void applyReaction(struct globalState& gState){

    if(gState.reactionType=='S'){
        stemIntoG(gState);
    }else if(gState.reactionType=='G'){
        gSplit(gState);
    }else if(gState.reactionType=='N'){
        death(gState);
    }

}

void checkTerminalState(struct globalState& gState, struct CFG& cfg){

    if(gState.t > cfg.maxTime){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max time\n";
    }else if( (gState.nS+gState.nG+gState.nN)==maxIndividuals ){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max population\n";
    }
}

void agingProcess(struct globalState& gState, struct CFG& cfg){

    int agedCellsCount = 0;
    int agedCellsNumber = gState.nG + gState.nN;

    for(int i=0; i<maxIndividuals; i++){
        if(gState.populationArray[i].isAlive){
            char grp = gState.populationArray[i].group;
            if(grp=='G' || grp=='N'){

                gState.populationArray[i].age += gState.dt;

                agedCellsCount += 1;
                if(agedCellsCount == agedCellsNumber){
                    break;
                }
            }
        }
    }

}
