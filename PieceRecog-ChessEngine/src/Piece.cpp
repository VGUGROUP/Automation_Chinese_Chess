#include "Piece.h"


Piece::Piece(int _pieceType, int _pieceTeam, std::pair<int,int> _realPos)
{
    this->pieceType = _pieceType;
    
    if (_pieceTeam < 7)
    {
        this->pieceTeam = _pieceTeam;

    }
    else
    {
        this->pieceTeam = 4;
    }

    this->realPos = _realPos;

    if (this->pieceTeam == 1)
    {
        this->pieceName = "Red" + name[pieceType];
    }
    else
    {
        this->pieceName = "Black" + name[pieceType];
    }
    
    this->boardPos = std::make_pair((int)(_realPos.first/pieceWidth) +1, 8 - (int)(_realPos.second/pieceWidth) +1);
}

void Piece::setType(int _pieceType)
{
    this->pieceType = _pieceType;
    if (this->pieceTeam == 1)
    {
        this->pieceName = "Red" + name[pieceType];
    }
    else
    {
        this->pieceName = "Black" + name[pieceType];
    }
}

std::string Piece::getName()
{
    return pieceName;
}

std::pair<int,int> Piece::getBoardPos()
{
    return boardPos;
}

std::pair<int,int> Piece::getRealPos()
{
    return realPos;
}

int Piece::getType()
{
    return pieceType;
}