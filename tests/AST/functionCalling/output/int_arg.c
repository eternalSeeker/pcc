FileAST: 
  Decl: test, [], [], []
    FuncDecl: 
      ParamList: 
        Decl: i, [], [], []
          TypeDecl: i, []
            IdentifierType: ['int']
      TypeDecl: test, []
        IdentifierType: ['void']
  Decl: test2, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: test2, []
        IdentifierType: ['void']
  FuncDef: 
    Decl: test, [], [], []
      FuncDecl: 
        ParamList: 
          Decl: i, [], [], []
            TypeDecl: i, []
              IdentifierType: ['int']
        TypeDecl: test, []
          IdentifierType: ['void']
    Compound: 
      Decl: foo, [], [], []
        TypeDecl: foo, []
          IdentifierType: ['int']
  FuncDef: 
    Decl: test2, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: test2, []
          IdentifierType: ['void']
    Compound: 
      Decl: arg, [], [], []
        TypeDecl: arg, []
          IdentifierType: ['int']
        Constant: int, 1
      FuncCall: 
        ID: test
        ExprList: 
          ID: arg
