FileAST: 
  Decl: test, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: test, []
        IdentifierType: ['char']
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
          IdentifierType: ['char']
    Compound: 
      Decl: foo, [], [], []
        TypeDecl: foo, []
          IdentifierType: ['char']
        Constant: int, 21
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
