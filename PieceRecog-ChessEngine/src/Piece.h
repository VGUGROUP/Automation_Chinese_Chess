#include <iostream>
#include <sstream>
#include <string>
#include <opencv2/core.hpp>



class Piece
{
private:
    std::string pieceName;
    int pieceType;
    int pieceTeam;
    
    std::pair<int,int> boardPos;
    std::pair<int,int> realPos;
    std::vector<std::string> name = {"Cannon","Car","Horse","Elephant","Advisor","General","Soldier"};

    int pieceWidth = 115;
public:
    Piece(int pieceType, int pieceTeam, std::pair<int,int> realPos);
    std::pair<int,int> getRealPos();
    std::pair<int,int> getBoardPos();
    
    void setType(int _pieceType);
    std::string getName();
    int getType();
};

