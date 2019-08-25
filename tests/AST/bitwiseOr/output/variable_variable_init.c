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
      Decl: q, [], [], []
        TypeDecl: q, []
          IdentifierType: ['char']
        Constant: int, 2
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['char']
        BinaryOp: |
          ID: p
          ID: q
