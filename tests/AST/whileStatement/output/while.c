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
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
        Constant: int, 10
      While: 
        ID: i
        Compound: 
          Assignment: =
            ID: i
            BinaryOp: -
              ID: i
              Constant: int, 1
