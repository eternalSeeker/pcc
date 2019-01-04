FileAST: 
  Decl: test, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
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
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
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
      FuncCall: 
        ID: test
