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
    int randSeed;
    float dJ = 0.0060455567;
    float dA = 0.27;
    float beta = 8.5;
    float c = 600;
    float tau = 15.6;
    int J0 = 0;
    int A0 = 5000;
    float maxTime = 120;
};

struct iState{
    // Defaults to dead, without id
    int id;
    bool isAlive = false;
    float age = 0;
    char group = 'J';
};

// propensity functions
float birthRate(struct CFG cfg, struct iState s, int nJ, int nA){

    if(s.isAlive){
        if(s.group=='J'){
            return 0;
        }
        else{
            //  if(s.group=='A')
            return cfg.beta*exp(-nA/cfg.c);
        }
    }else{
        return 0;
    }

}

float deathRate(struct CFG cfg, struct iState s, int nJ, int nA){

    if(s.isAlive){
        if(s.group=='J'){
            return cfg.dJ;
        }
        else{
            //  if(s.group=='A')
            return cfg.dA;
        }
    }else{
        return 0;
    }

}

float maturationRate(struct CFG cfg, struct iState s){

    float rate = 0;
    if(s.isAlive){
        if(s.group=='J'){
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

    int nJ;
    int nA;
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
    for(int i=0; i<cfg.J0; i++){
        gState.populationArray[i].id = i;
        gState.populationArray[i].isAlive = true;
        gState.populationArray[i].group='J';
        gState.populationArray[i].age = 0;
    }
    for(int i=0; i<cfg.A0; i++){
        gState.populationArray[cfg.J0+i].id = i;
        gState.populationArray[cfg.J0+i].isAlive = true;
        gState.populationArray[cfg.J0+i].group='A';
        gState.populationArray[cfg.J0+i].age = cfg.tau;
    }
    gState.nJ = cfg.J0;
    gState.nA = cfg.A0;

    // Init reaction array, propensity array and total propensity
    float totProp = 0;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float bRate = birthRate(cfg, s, cfg.J0, cfg.A0);
        gState.reactionArray[maxReactions*i + 0].indivId = i;
        gState.reactionArray[maxReactions*i + 0].type = '+';
        gState.reactionArray[maxReactions*i + 0].propensity = bRate;
        totProp += bRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float dRate = deathRate(cfg, s, cfg.J0, cfg.A0);
        gState.reactionArray[maxReactions*i + 1].indivId = i;
        gState.reactionArray[maxReactions*i + 1].type = '-';
        gState.reactionArray[maxReactions*i + 1].propensity = dRate;
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

        float mRate = maturationRate(cfg, s);
        gState.reactionArray[maxReactions*i + 2].indivId = i;
        gState.reactionArray[maxReactions*i + 2].type = 'm';
        gState.reactionArray[maxReactions*i + 2].propensity = mRate;
        totProp += mRate;
        gState.propensityArray[maxReactions*i + 2] = totProp;

    }
    gState.totPropensity = totProp;

}

void printGlobalState(struct globalState gState){

    if(!gState.isTerminalState){

            cout << "t: " << gState.t << " nJ: " << gState.nJ << " nA: " << gState.nA << '\n';

            string populationAliveLog = "";
            int aliveCount = 0;
            for(int i=0; i<maxIndividuals; i++){
                if(gState.populationArray[i].isAlive){
                    if(gState.populationArray[i].group == 'J'){
                        populationAliveLog += 'J';
                    }else{
                        populationAliveLog += 'A';
                    }
                    aliveCount += 1;
                }else{
                    populationAliveLog += '_';
                }
                if(aliveCount==(gState.nJ+gState.nA)){
                    break;
                }
            }
            cout << gState.t << " " << populationAliveLog << '\n';
    }else{
        cout << gState.terminalLog;
    }

}

void printCsvLine(struct globalState gState){
    cout << gState.t <<','<< gState.nJ <<','<< gState.nA <<'\n';
}

void updatePropensities(struct globalState& gState, struct CFG& cfg){

    float totProp = 0;
    int aliveCount = 0;
    int totIndividuals = gState.nJ + gState.nA;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float bRate = birthRate(cfg, s, gState.nJ, gState.nA);
        totProp += bRate;
        gState.propensityArray[maxReactions*i + 0] = totProp;

        float dRate = deathRate(cfg, s, gState.nJ, gState.nA);
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = totProp;

        float mRate = maturationRate(cfg, s);
        totProp += mRate;
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

void birth(struct globalState& gState){

    for(int i=0; i<maxIndividuals; i++){
        if( ! gState.populationArray[i].isAlive ){
            gState.populationArray[i].isAlive = true;
            gState.populationArray[i].group = 'J';
            gState.populationArray[i].age = 0;
            gState.nJ += 1;
            break;
        }
    }
}

void death(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;
    gState.populationArray[indivId].isAlive = false;
    if(gState.populationArray[indivId].group == 'J'){
        gState.nJ += -1;
    }else if(gState.populationArray[indivId].group == 'A'){
        gState.nA += -1;
    }

}

void maturation(struct globalState& gState){

    int indivId = gState.reactionArray[gState.reactionIdx].indivId;

    gState.populationArray[indivId].group = 'A';
    gState.nJ += -1;
    gState.nA += 1;

}

void applyReaction(struct globalState& gState){

    if(gState.reactionType=='+'){
        birth(gState);
    }else if(gState.reactionType=='-'){
        death(gState);
    }else if(gState.reactionType=='m'){
        maturation(gState);
    }

}

void checkTerminalState(struct globalState& gState, struct CFG& cfg){

    if(gState.t > cfg.maxTime){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max time\n";
    }else if(gState.nJ==0 && gState.nA==0){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: extinction\n";
    }else if( (gState.nJ+gState.nA)==maxIndividuals ){
        gState.isTerminalState = true;
        gState.terminalLog = "End of simulation: max population\n";
    }
}

void updateAge(struct globalState& gState, struct CFG& cfg){

    int juvenilesCount = 0;
    int juvenilesNumber = gState.nJ;

    for(int i=0; i<maxIndividuals; i++){
        if(gState.populationArray[i].isAlive){
            if(gState.populationArray[i].group == 'J'){

                gState.populationArray[i].age += gState.dt;

                juvenilesCount += 1;
                if(juvenilesCount == juvenilesNumber){
                    break;
                }
            }
        }
    }

}
