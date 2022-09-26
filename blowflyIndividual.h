#include <iostream>
#include <random>
#include <string>

using namespace std;

// constants
const int maxIndividuals = 500;
const int maxReactions = 2;

struct CFG{
    // config
    float r = 1;
    float K = 10;
    int N0 = 10;
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

    float t = 0;
    float dt;
    int reactionIdx;
    char reactionType;

    bool isTerminalState = false;
    string terminalLog;

};

void initGlobalState(struct CFG cfg, struct globalState& gState){

    // Init population array and populations number
    for(int i=0; i<cfg.N0; i++){
        gState.populationArray[i].id = i;
        gState.populationArray[i].isAlive = true;
    }
    gState.N = cfg.N0;

    // Init reaction array, propensity array and total propensity
    float totProp = 0;
    for(int i=0; i<cfg.N0; i++){

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

    cout << "t: " << gState.t << " N: " << gState.N << '\n';

    string populationAliveLog = "";
    for(int i=0; i<gState.N; i++){
        if(gState.populationArray[i].isAlive){
            populationAliveLog += '*';
        }else{
            populationAliveLog += '_';
        }
    }
    cout << populationAliveLog << '\n';


    string reactionTypeLog = "";
    string reactionPropLog = "";
    for(int i=0; i<gState.N*2; i++){
        reactionTypeLog += gState.reactionArray[i].type;
        reactionPropLog += to_string(gState.propensityArray[i])+" ";
    }
    cout << reactionTypeLog << '\n';
    cout << reactionPropLog << '\n';


}

void printCsvLine(struct globalState gState){
    cout << gState.t <<','<<gState.N<<'\n';
}

void updatePropensities(struct globalState& gState, struct CFG& cfg){

    float totProp = 0;
    int aliveCount = 0;
    for(int i=0; i<maxIndividuals; i++){

        iState s = gState.populationArray[i];

        float bRate = birthRate(cfg, s, gState.N);
        totProp += bRate;
        gState.propensityArray[maxReactions*i + 0] = bRate;

        float dRate = deathRate(cfg, s, gState.N);
        totProp += dRate;
        gState.propensityArray[maxReactions*i + 1] = dRate;

        if(s.isAlive){
            aliveCount += 1;
            if(aliveCount==gState.N){
                break;
            }
        }

    }
    gState.totPropensity = totProp;

}

float drawFromUniform01(int maxInt){
    // This should return a random number between 0 and 1 with enough "resolution"
    // for not "missing" or "skipping" any propensity interval.
    // Now, my approach is to take the smallest interval Dp that I want to "see"
    // and choosing maxInt as 10 * 1/Dp
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, maxInt-1);

    float r1;
    r1 = dis(gen)/float(maxInt);

    return r1;

}
