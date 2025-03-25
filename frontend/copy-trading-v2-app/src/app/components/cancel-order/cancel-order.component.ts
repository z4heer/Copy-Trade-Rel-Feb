import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cancel-order',
  templateUrl: './cancel-order.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [ReactiveFormsModule, CommonModule]
})
export class CancelOrderComponent implements OnInit {
  cancelOrderForm: FormGroup;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private tradeService: TradeService
  ) {
    this.cancelOrderForm = this.fb.group({
      userid: ['45937331', Validators.required],
      Trading_Symbol: ['', Validators.required],
      Exchange: ['NSE', Validators.required],
      Action: ['BUY', Validators.required],
      Order_Type: ['LIMIT', Validators.required],
      CurrentQuantity: [1, Validators.required],
      Streaming_Symbol: ['', Validators.required],
      Order_ID: ['', Validators.required],
      Product_Code: ['CNC', Validators.required]
    });
  }

  ngOnInit(): void {}

  cancelOrder(): void {
    if (this.cancelOrderForm.invalid) {
      this.error = 'Cancel order form is invalid';
      return;
    }

    const orderDetails = this.cancelOrderForm.value;
    this.tradeService.cancelOrder(orderDetails).subscribe(
      () => {
        this.error = null;
        alert('Order canceled successfully');
      },
      (error) => {
        this.error = 'Failed to cancel order';
        console.error(error);
      }
    );
  }
}