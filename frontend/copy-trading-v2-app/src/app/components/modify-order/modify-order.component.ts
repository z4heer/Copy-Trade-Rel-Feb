import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-modify-order',
  templateUrl: './modify-order.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [ReactiveFormsModule, CommonModule]
})
export class ModifyOrderComponent implements OnInit {
  modifyOrderForm: FormGroup;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private tradeService: TradeService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.modifyOrderForm = this.fb.group({
      Action: [{ value: '' }],
      Exchange: [{ value: ''}],
      userid : [{ value: ''}],
      symbol: [{ value: ''}],
      Order_Type: ['LIMIT'],
      Quantity: [0],
      CurrentQuantity: [0],
      Limit_Price: [0],
      ProductCode: [''],
      Duration: [{ value: '' }],
      Trading_Symbol: [{ value: '' }],
      Streaming_Symbol: [{ value: '' }],
      Order_ID: [{ value: '' }],
      Disclosed_Quantity: [0]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const orderData = params['order'];
      if (orderData) {
        const order = JSON.parse(orderData);
        //console.log('ngOnInit()-order', order); // Correct logging
        this.populateForm(order);
      } else {
        console.error('No order data found in route parameters');
      }
    });
  }

  populateForm(order: any): void {
    console.log("populateForm()- "+order.userid);
    this.modifyOrderForm.patchValue({
      Action: order.Action,
      userid: order.userid,
      Exchange: order.Exchange,
      symbol: order.Symbol,
      Order_Type: order.Order_Type,
      Quantity: order.Quantity,
      CurrentQuantity: order.CurrentQuantity,
      Limit_Price: order.Limit_Price,
      ProductCode: order.Product_Code,
      Duration: order.Duration,
      Trading_Symbol: order.Trading_Symbol,
      Streaming_Symbol: order.Streaming_Symbol,
      Order_ID: order.Order_ID,      
      Disclosed_Quantity: order.Disclosed_Quantity
    });
  }

  modifyOrder(): void {
    if (this.modifyOrderForm.invalid) {
      this.error = 'Modify order form is invalid';
      return;
    }

    const orderDetails = this.modifyOrderForm.value;
    this.tradeService.modifyOrder(orderDetails).subscribe(
      () => {
        this.error = null;
        alert('Order modified successfully');
        this.router.navigate(['/orders']);
      },
      (error) => {
        this.error = 'Failed to modify order';
        console.error(error);
      }
    );
  }
}