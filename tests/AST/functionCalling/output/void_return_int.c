FileAST: 
  Decl: test, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: test, []
        IdentifierType: ['int']
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
          IdentifierType: ['int']
    Compound: 
      Decl: foo, [], [], []
        TypeDecl: foo, []
          IdentifierType: ['int']
        Constant: int, 5
      Return: 
        ID: foo
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
