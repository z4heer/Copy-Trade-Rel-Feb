import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-place-trade',
  templateUrl: './place-trade.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [ReactiveFormsModule, CommonModule]
})
export class PlaceTradeComponent implements OnInit {
  tradeForm: FormGroup;
  currentLtp: number | null = null;
  error: string | null = null;
  loading: boolean = false;
  constructor(
    private fb: FormBuilder,
    private tradeService: TradeService,
    private router: Router
  ) {
    this.tradeForm = this.fb.group({
      symbol: ['', Validators.required],
      Trading_Symbol: ['', Validators.required],
      Streaming_Symbol: ['', Validators.required],
      Exchange: ['NSE', Validators.required],
      Action: ['BUY', Validators.required],
      ProductCode: ['CNC', Validators.required],
      Order_Type: ['LIMIT', Validators.required],
      Quantity: [1, [Validators.required, Validators.min(1)]],
      Limit_Price: [0, Validators.required],
      Duration: ['DAY', Validators.required],
      Disclosed_Quantity: [0]
    });
  }

  ngOnInit(): void {
    //this.tradeForm.get('Trading_Symbol')?.disable()
    //this.tradeForm.get('Streaming_Symbol')?.disable()
    this.tradeForm.get('symbol')?.valueChanges.subscribe(symbol => {
      if (symbol) {
        this.tradeService.getIsin(symbol).subscribe(
          (response: any) => {
            //console.log(response);
          if (response && response.isin) {
              this.tradeForm.patchValue({ Trading_Symbol: response.isin }, { emitEvent: false });
              this.tradeForm.patchValue({ Streaming_Symbol: response.isin }, { emitEvent: false });
            } else {
              this.tradeForm.patchValue({ Trading_Symbol: '' }, { emitEvent: false });
              this.tradeForm.patchValue({ Streaming_Symbol: '' }, { emitEvent: false });
              this.error = 'ISIN not found';
            }
          },
          (error) => {
            this.tradeForm.patchValue({ isin: '' }, { emitEvent: false });
            this.error = 'Failed to fetch ISIN';
            console.error(error);
          }
        );
      }
    });
        
  }

  placeTrade(): void {
    this.loading = true;
    if (this.tradeForm.invalid) {
      this.error = 'Trade form is invalid';
      return;
    }
    //console.log(this.tradeForm.value);
    const tradeDetails = this.tradeForm.value;
    this.tradeService.placeTrade(tradeDetails).subscribe(
      () => {
        this.error = null;
        alert('Trade placed successfully');
        this.loading = false;
        this.router.navigate(['/orders']);

      },
      (error) => {
        this.loading=false;
        this.error = 'Failed to place trade, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }
}