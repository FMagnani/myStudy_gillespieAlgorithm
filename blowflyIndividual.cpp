#include <iostream>
#include "blowflyIndividual.h"

using namespace std;

int main(){

    CFG cfg;
    globalState gState;

    initGlobalState(cfg, gState);

    printGlobalState(gState);

    // simulate death of third individual
    gState.populationArray[2].isAlive = false;
    gState.N -= 1;

    printGlobalState(gState);

    updatePropensities(gState, cfg);

    printGlobalState(gState);


/*
    float Dp = 0.009;
    int maxInt = int(10/0.009);

    cout << maxInt << '\n';
    cout << drawFromUniform01(maxInt) << '\n';
*/

//    Individual i = Individual(1);
//    cout << i.birthRate(cfg, 10) << '\n';
//    cout << i.deathRate(cfg, 10) << '\n';

}
