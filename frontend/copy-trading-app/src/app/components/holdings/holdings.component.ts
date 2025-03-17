import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Holding, HoldingResponse } from '../net-positions/position.model';

@Component({
  selector: 'app-holdings',
  templateUrl: './holdings.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule]
})
export class HoldingsComponent implements OnInit {
  holdings: Holding[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService) {}

  ngOnInit(): void {
    this.tradeService.getHoldings_all().subscribe(
      data => this.holdings = data.Holdings,
      (error) => {
        this.error = 'Failed to load holdings, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  call_squareoff(holding: Holding): void {
  
    const holdingData = JSON.stringify(holding);
  }
  
    squareOff(holding: any): void {
    const positionDetails = {
      userid: '45937331',
      sqrLst: [
        {
          TradingSymbol: holding.symbol,
          Exchange: 'NSE',
          Action: 'SELL',
          Duration: 'DAY',
          OrderType: 'LIMIT',
          Quantity: holding.quantity,
          ProductCode: 'CNC',
          StreamingSymbol: holding.symbol,
          Price: holding.price,
          DisclosedQuantity: 0,
          GTDDate: 'NA',
          Remark: 'Closing positions',
          TriggerPrice: holding.price
        }
      ]
    };

    this.tradeService.squareOff(positionDetails).subscribe(
      () => {
        alert('Position squared off successfully');
      },
      (error) => {
        this.error = 'Failed to square off position';
        console.error(error);
      }
    );
  }
}