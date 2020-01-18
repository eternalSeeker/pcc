FileAST: 
  Decl: putchar, [], [], []
    FuncDecl: 
      ParamList: 
        Decl: c, [], [], []
          TypeDecl: c, []
            IdentifierType: ['int']
      TypeDecl: putchar, []
        IdentifierType: ['int']
  Decl: main, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: main, []
        IdentifierType: ['void']
  Decl: fac, [], [], []
    FuncDecl: 
      ParamList: 
        Decl: i, [], [], []
          TypeDecl: i, []
            IdentifierType: ['int']
      TypeDecl: fac, []
        IdentifierType: ['int']
  FuncDef: 
    Decl: fac, [], [], []
      FuncDecl: 
        ParamList: 
          Decl: i, [], [], []
            TypeDecl: i, []
              IdentifierType: ['int']
        TypeDecl: fac, []
          IdentifierType: ['int']
    Compound: 
      Decl: j, [], [], []
        TypeDecl: j, []
          IdentifierType: ['int']
      If: 
        BinaryOp: >
          ID: i
          Constant: int, 1
        Compound: 
          Decl: c, [], [], []
            TypeDecl: c, []
              IdentifierType: ['int']
            BinaryOp: -
              ID: i
              Constant: int, 1
          Assignment: =
            ID: j
            FuncCall: 
              ID: fac
              ExprList: 
                ID: c
          Assignment: =
            ID: j
            BinaryOp: *
              ID: j
              ID: i
          Return: 
            ID: j
      Return: 
        Constant: int, 1
  FuncDef: 
    Decl: main, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: main, []
          IdentifierType: ['void']
    Compound: 
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['int']
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
      Assignment: =
        ID: c
        Constant: int, 4
      Assignment: =
        ID: i
        FuncCall: 
          ID: fac
          ExprList: 
            ID: c
      Assignment: =
        ID: c
        BinaryOp: -
          ID: i
          Constant: int, 24
      If: 
        ID: c
        Compound: 
          Assignment: =
            ID: c
            Constant: char, 'N'
          FuncCall: 
            ID: putchar
            ExprList: 
              ID: c
      Assignment: =
        ID: c
        Constant: char, 'H'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'e'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'l'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'l'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'o'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: int, 32
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'W'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'o'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'r'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'l'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, 'd'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Assignment: =
        ID: c
        Constant: char, '\n'
      FuncCall: 
        ID: putchar
        ExprList: 
          ID: c
      Return: 
