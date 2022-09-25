#include <iostream>
#include "blowflyIndividual.h"

using namespace std;

// constants
const int maxIndividuals = 500;

// config
struct CFG{

    float birthRate = 1;
    float deathRate = 10;

} cfg;

// global state - this is continuously changed
struct globalState{

    float populationArray[maxIndividuals];

} gState;

class Individual{
public:
    struct iState{
        int id;
        bool isAlive;
    } s;
    Individual(int id, bool isAlive=true){
        s.id = id;
        s.isAlive = isAlive;
    };

    float birthRate(struct CFG cfg, int nJ, int nA){
        if(s.isAlive){
            return cfg.birthRate;
        }else{
            return 0;
        }
    }

    float deathRate(struct CFG cfg, int nJ, int nA){
        if(s.isAlive){
            return cfg.deathRate;
        }else{
            return 0;
        }
    }

};

int main(){

/*
    float Dp = 0.009;
    int maxInt = int(10/0.009);

    cout << maxInt << '\n';
    cout << drawFromUniform01(maxInt) << '\n';
*/

    Individual i = Individual(1);
    cout << i.birthRate(cfg, 10, 10) << '\n';
    cout << i.deathRate(cfg, 10, 10) << '\n';

}
