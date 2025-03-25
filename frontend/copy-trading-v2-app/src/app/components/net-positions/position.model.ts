export interface Holding {
  userid: string;
  Symbol: string;
  TradingSymbol: string;
  Exchange: string;
  BuyQuantity: number;
  BuyPrice: number;
  TotalVal: string;
  Ltp: string;
  ChangePcToday: string;
  ProductCode: string;
  StreamingSymbol: string;
  }
  
  export interface HoldingResponse {
    Holdings: Holding[];
  }

  export interface Position {
    TradingSymbol: string;
    Exchange: string;
    BuyQuantity: number;
    SellQuantity: number;
    BuyPrice: string;
    SellPrice: string;
    ProductCode: string;
    StreamingSymbol: string;
    squareOffSts: string;
    squareOffAction: string;
    userid: string;
    Symbol: string;
  }
  
  export interface NetPositionResponse {
    Positions: Position[];
  }
  