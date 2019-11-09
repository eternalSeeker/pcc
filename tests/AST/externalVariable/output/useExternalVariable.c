FileAST: 
  Decl: integer, [], ['extern'], []
    TypeDecl: integer, []
      IdentifierType: ['int']
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
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
        Constant: int, 0
      Decl: j, [], [], []
        TypeDecl: j, []
          IdentifierType: ['int']
      Assignment: =
        ID: integer
        ID: i
      Assignment: =
        ID: j
        ID: integer
