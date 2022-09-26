#include <iostream>
#include "blowflyIndividual.h"

using namespace std;

int main(){

    CFG cfg;
    globalState gState;

    initGlobalState(cfg, gState);
    printCsvLine(gState);
    printCsvLine(gState);
    printCsvLine(gState);

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
