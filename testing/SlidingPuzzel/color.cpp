// def colorTransform(colors,weight):
//     coror1 = colors[0]
//     coror2 = colors[1]
//     r = coror1[0]*weight + coror2[0]*(1-weight)
//     g = coror1[1]*weight + coror2[1]*(1-weight)
//     b = coror1[2]*weight + coror2[2]*(1-weight)
//     return r,g,b
#include <iostream>
using namespace std;

struct colorValue {
    int r;
    int g;
    int b;
} my;

colorValue colorTransform(colorValue color1,colorValue color2, float weagit){


}






int main() {
    colorValue my;
    my.r = 1;
    my.g = 2;
    my.b = 3;
    cout << my.r << "\n";

    return 0;
}