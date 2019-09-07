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
      Decl: p, [], [], []
        TypeDecl: p, []
          IdentifierType: ['char']
        Constant: int, 1
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['char']
        Constant: int, 0
      Assignment: =
        ID: c
        BinaryOp: >
          ID: p
          Constant: int, 2
