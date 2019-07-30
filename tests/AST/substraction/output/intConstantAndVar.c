FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: foo, []
        IdentifierType: ['void']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: foo, []
          IdentifierType: ['void']
    Compound: 
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['int']
        Constant: int, 0
      Decl: d, [], [], []
        TypeDecl: d, []
          IdentifierType: ['int']
        Constant: int, 2
      Assignment: =
        ID: c
        BinaryOp: -
          Constant: int, 1
          ID: d
