import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { ModifyOrderComponent } from '../modify-order/modify-order.component';
import { CancelOrderComponent } from '../cancel-order/cancel-order.component';

@Component({
  selector: 'app-trades',
  templateUrl: './trades.component.html',
  standalone: true,
  providers: [TradeService, ModifyOrderComponent,CancelOrderComponent],
  imports: [CommonModule]
})
export class TradesComponent implements OnInit {
  orders: any[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService) {}

  ngOnInit(): void {
    this.tradeService.getTrades().subscribe(
      (data) => {
        if (typeof data === 'string') {
          try {
            console.log("typeof data === string");
            this.orders = JSON.parse(data).orders;

          } catch (e) {
            console.error('Failed to parse JSON data:', e);
            this.error = 'Failed to load orders';
            return;
          }
        } else {
          this.orders = data;
        }
        console.log("data.length= " + this.orders.length);
      },
      (error) => {
        this.error = 'Failed to load Trades, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  squareOff(order: any): void {
    // Implement the logic to modify the order here
    console.log('Position squareOff():', order);
  }

}

