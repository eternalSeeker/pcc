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
      Decl: f, [], [], []
        TypeDecl: f, []
          IdentifierType: ['float']
        Constant: double, 0.0
      Assignment: =
        ID: f
        BinaryOp: +
          Constant: double, 1.23
          Constant: double, 9.87
