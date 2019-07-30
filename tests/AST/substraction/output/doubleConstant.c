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
      Decl: d, [], [], []
        TypeDecl: d, []
          IdentifierType: ['double']
        Constant: double, 0.0
      Assignment: =
        ID: d
        BinaryOp: -
          Constant: double, 4.44
          Constant: double, 2.21
