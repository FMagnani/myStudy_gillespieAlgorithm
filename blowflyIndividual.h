#include <iostream>
#include <random>

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


/*
void drawFromUniform01(struct globalState& gState, int idx){

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 9999);

    float r1;
    r1 = dis(gen)/float(10000);

    gState.populationArray[idx] = r1;

}
*/
