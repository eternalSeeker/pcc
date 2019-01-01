FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Decl: i, [], [], []
          TypeDecl: i, []
            IdentifierType: ['int']
        Decl: c, [], [], []
          TypeDecl: c, []
            IdentifierType: ['char']
      TypeDecl: foo, []
        IdentifierType: ['void']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Decl: i, [], [], []
            TypeDecl: i, []
              IdentifierType: ['int']
          Decl: c, [], [], []
            TypeDecl: c, []
              IdentifierType: ['char']
        TypeDecl: foo, []
          IdentifierType: ['void']
    Compound: 
      Decl: a, [], [], []
        TypeDecl: a, []
          IdentifierType: ['int']
        Constant: int, 0
