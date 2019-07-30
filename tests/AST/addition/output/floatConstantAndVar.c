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
          IdentifierType: ['float']
        Constant: double, 0.0
      Decl: d, [], [], []
        TypeDecl: d, []
          IdentifierType: ['float']
        Constant: double, 2.0
      Assignment: =
        ID: c
        BinaryOp: +
          Constant: double, 1.0
          ID: d
