FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Decl: i, [], [], []
          TypeDecl: i, []
            IdentifierType: ['char']
      TypeDecl: foo, []
        IdentifierType: ['void']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Decl: i, [], [], []
            TypeDecl: i, []
              IdentifierType: ['char']
        TypeDecl: foo, []
          IdentifierType: ['void']
    Compound: 
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['int']
        Constant: int, 0
