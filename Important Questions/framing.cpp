#include <iostream>
#include <string>

using namespace std;

string bitStuffing(const string &data) {
    string flag = "01111110";
    string stuffedData = "";
    int count = 0;

    for (char bit : data) {
        if (bit == '1') {
            count++;
        } else {
            count = 0;
        }

        stuffedData += bit;
        if (count == 5) {
            stuffedData += '0';
            count = 0;
        }
    }

    return flag +" "+ stuffedData +" "+ flag;
}

string bitDestuffing(const string &data) {
    string flag = "01111110";
    string destuffedData = "";
    int count = 0;

    string message = data.substr(flag.length(), data.length() - 2 * flag.length());

    for (char bits:message) {
        if (bits == '1') {
            count++;
            destuffedData += bits;
        } 
        else{
            if (count == 5){
                count = 0;
                continue;
            }
            destuffedData += bits;
            count = 0;
            
        }
        
    }
    return destuffedData;
}

int main(){
    string choice;
    cout << "Enter your string:";
    cin >> choice;
    string message = bitStuffing(choice);
    cout << "Stuffed data is: "<< message<<endl;

    cout << "DeStuffed data is: "<< bitDestuffing(message)<< endl;

}