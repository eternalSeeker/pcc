FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: foo, []
        IdentifierType: ['int']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: foo, []
          IdentifierType: ['int']
    Compound: 
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
        Constant: int, 0
      If: 
        Constant: int, 1
        Compound: 
          Assignment: =
            ID: i
            Constant: int, 5
      Decl: j, [], [], []
        TypeDecl: j, []
          IdentifierType: ['int']
        Constant: int, 0
      Decl: c, [], [], []
        TypeDecl: c, []
          IdentifierType: ['char']
        Constant: int, 12
      Return: 
        ID: i
