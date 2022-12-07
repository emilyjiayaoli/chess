def isWhiteDuringCheck(self):
        assert(self.isCheck == True)
        if self.colorChecking == "whiteChecking":
            return True
        else: return False

def getAllLegalMoves(self):
    # gets legal moves for all pieces
    for r in range(len(self.board)):
        for c in range(len(self.board[0])):
            piece = self.board[r][c]
            if piece != None:
                if self.isCheck:
                    boardObj = copy.deepcopy(self)
                    boardObj.isCheck = False # set is check back to false
                    boardObj.mode = "pseudo"
                    #print(self.mode, boardObj.mode)
                    if piece.name != "king":
                        if self.colorChecking == "whiteChecking":
                            if not piece.isWhite:
                                pieceInBoardObj = boardObj.board[r][c]
                                #piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                                fullMoves = piece.legalMoves
                                protectionMoves = piece.getLegalMovesDuringCheck(boardObj, fullMoves)
                                piece.legalMoves = protectionMoves
                                #pieceInBoardObj.legalMoves = protectionMoves

                        elif self.colorChecking == "blackChecking":
                            if piece.isWhite:
                                pieceInBoardObj = boardObj.board[r][c]
                                #piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                                fullMoves = piece.legalMoves
                                protectionMoves = piece.getLegalMovesDuringCheck(boardObj, fullMoves)
                                piece.legalMoves = protectionMoves
                                #pieceInBoardObj.legalMoves = protectionMoves
                        else:
                            raise AssertionError("self.colorChecking is neither white or black")
            
                else:
                    piece.legalMoves = piece.getLegalMoves(self)

def getAllLegalMovesInPseudo(self):
    # gets legal moves for all pieces
    for r in range(len(self.board)):
        for c in range(len(self.board[0])):
            piece = self.board[r][c]
            if piece != None:
                if self.isCheck and self.mode != "pseudo":
                    boardObj = copy.deepcopy(self)
                    #boardObj.isCheck = False # set is check back to false
                    boardObj.mode = "pseudo"
                    #print(self.mode, boardObj.mode)
                    if piece.name != "king":
                        if self.colorChecking == "whiteChecking":
                            if not piece.isWhite:
                                pieceInBoardObj = boardObj.board[r][c]
                                #piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                                fullMoves = piece.legalMoves
                                protectionMoves = piece.getLegalMovesDuringCheck(boardObj, fullMoves)
                                piece.legalMoves = protectionMoves
                                #pieceInBoardObj.legalMoves = protectionMoves

                        elif self.colorChecking == "blackChecking":
                            if piece.isWhite:
                                pieceInBoardObj = boardObj.board[r][c]
                                #piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                                fullMoves = piece.legalMoves
                                protectionMoves = piece.getLegalMovesDuringCheck(boardObj, fullMoves)
                                piece.legalMoves = protectionMoves
                                #pieceInBoardObj.legalMoves = protectionMoves
                        else:
                            raise AssertionError("self.colorChecking is neither white or black")
                    else: #king in check
                        if self.mode == "pseudo":
                            piece.legalMoves = piece.getLegalMoves(self)
                        else:
                            piece.legalMoves = piece.getLegalMoves(self)
                    # del boardObj
                else:
                    piece.legalMoves = piece.getLegalMoves(self)
                    