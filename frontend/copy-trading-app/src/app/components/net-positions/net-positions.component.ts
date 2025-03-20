import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { NetPositionResponse, Position } from './position.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-net-positions',
  templateUrl: './net-positions.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule]
})
export class NetPositionsComponent implements OnInit {
  positions: Position[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService, private router: Router) {}

  ngOnInit(): void {
    this.tradeService.getNetPositions().subscribe(
      (data: NetPositionResponse) => {
        if (data && data.Positions) {
          this.positions = data.Positions;
          console.log("data.length= ", this.positions.length);
        } else {
          console.error("Data format is incorrect");
        }
      },
      (error) => {
        this.error = 'Failed to load Net Positions, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }
  
  call_squareoff(position: Position): void {
    //console.log('Sqaure off- order:', position);
    const positionData = JSON.stringify(position);
    this.router.navigate(['/square-off-position', { position: positionData }]);
  }
  
  squareOff(holding: any): void {
    const positionDetails = {
      userid: holding,
      sqrLst: [
        {
          TradingSymbol: holding.Trading_Symbol,
          Exchange: holding.Exchange,
          Action: 'SELL',
          Duration: 'DAY',
          OrderType: 'LIMIT',
          Quantity: holding.quantity,
          ProductCode: 'CNC',
          StreamingSymbol: holding.Streaming_Symbol,
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