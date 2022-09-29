#include <iostream>
#include "blowflyIndividual.h"

using namespace std;


int main(){

    CFG cfg;
    globalState gState;

    mt19937 gen(cfg.randSeed); // Standard mersenne_twister_engine
    uniform_real_distribution<> distr(0.0, 1.0);

    initGlobalState(gState, cfg);
    //printGlobalState(gState);

    while( !gState.isTerminalState ){

        float r1 = distr(gen);
        float r2 = distr(gen);

        selectTime(gState, r1);
        selectReaction(gState, r2);

        maturationProcess(gState, cfg);

        applyReaction(gState);

        checkTerminalState(gState, cfg);

        if( !gState.isTerminalState ){
            updatePropensities(gState, cfg);
        }

        //printGlobalState(gState);
        printCsvLine(gState);

    }



}
