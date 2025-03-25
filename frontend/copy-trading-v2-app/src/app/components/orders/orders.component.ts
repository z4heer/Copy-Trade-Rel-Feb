import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule]
})

export class OrdersComponent implements OnInit {
  orders: any[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService, private router: Router) {}

  ngOnInit(): void {
    this.tradeService.getOrders().subscribe(
      (data) => {
        if (typeof data === 'string') {
          try {
            console.log("typeof data === string");
            //console.log("data= " + data); 
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
        this.error = 'Failed to load orders, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  modifyOrder1(order: any): void {
    console.log('Modify order:', order);
    this.router.navigate(['/modify-order'], { state: { order } });
  }
  modifyOrder(order: any): void {
    //console.log('Modify order- order.Symbol:', order.Symbol);
    const orderData = JSON.stringify(order);
    this.router.navigate(['/modify-order', { order: orderData }]);
  }

  cancelOrder(order: any): void {
    const orderDetails = {
      userid: order.userid,
      Trading_Symbol: order.Trading_Symbol,
      Exchange: order.Exchange,
      Action: order.Action,
      Order_Type: order.Order_Type,
      Streaming_Symbol: order.Streaming_Symbol,
      Order_ID: order.Order_ID,
      Product_Code: order.Product_Code,
      CurrentQuantity: order.CurrentQuantity
    };

    const confirmation = confirm('Are you sure you want to cancel the order?');
    if (confirmation) {
      this.tradeService.cancelOrder(orderDetails).subscribe({
        next: (response) => {
          console.log('Order Cancelled successfully:', response);
        },
        error: (error) => {
          console.error('Error Cancel order:', error);
        }
      });
    } else {
      console.log('Order cancellation aborted.');
    }
  }

}