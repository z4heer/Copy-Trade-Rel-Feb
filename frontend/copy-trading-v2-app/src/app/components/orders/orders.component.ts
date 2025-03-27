import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule, FormsModule]
})

export class OrdersComponent implements OnInit {
  orders: any[] = [];
  filteredOrders: any[] = [];
  error: string | null = null;
  loading: boolean = false;
  filterSymbol: string = '';
  sortField: string = '';
  sortOrder: string = 'asc';

  constructor(private tradeService: TradeService, private router: Router) {}

  ngOnInit(): void {
	this.loading = true;
    this.tradeService.getOrders().subscribe(
      (data) => {
        if (typeof data === 'string') {
          try {
            this.loading = false;
			      this.orders = JSON.parse(data).orders;
          } catch (e) {
            console.error('Failed to parse JSON data:', e);
            this.error = 'Failed to load orders';
            return;
          }
        } else {
          this.orders = data;
        }
		this.loading = false;
        this.filteredOrders = [...this.orders];
      },
      (error) => {
        this.error = 'Failed to load orders, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  filterOrders(): void {
    this.filteredOrders = this.orders.filter(order =>
      order.Symbol.toLowerCase().includes(this.filterSymbol.toLowerCase())
    );
  }

  sortOrders(field: string): void {
    if (this.sortField === field) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortOrder = 'asc';
    }

    this.filteredOrders.sort((a, b) => {
      const valueA = a[field];
      const valueB = b[field];

      if (valueA < valueB) {
        return this.sortOrder === 'asc' ? -1 : 1;
      } else if (valueA > valueB) {
        return this.sortOrder === 'asc' ? 1 : -1;
      } else {
        return 0;
      }
    });
  }

  modifyOrder(order: any): void {
    const orderData = JSON.stringify(order);
    this.router.navigate(['/modify-order', { order: orderData }]);
  }

  cancelOrder(order: any): void {
	this.loading = true;
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
		  this.loading = false;
          console.log('Order Cancelled successfully:', response);
        },
        error: (error) => {
          console.error('Error Cancel order:', error);
        }
      });
    } else {
      console.log('Order cancellation aborted.');
    }
	this.loading = false;
   }
}