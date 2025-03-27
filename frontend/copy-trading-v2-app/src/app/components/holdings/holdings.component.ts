import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Holding } from '../net-positions/position.model';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-holdings',
  templateUrl: './holdings.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule, FormsModule]
})
export class HoldingsComponent implements OnInit {
  holdings: Holding[] = [];
  filteredHoldings: Holding[] = [];
  error: string | null = null;
  loading: boolean = false;
  filterSymbol: string = '';
  sortField: string = '';
  sortOrder: string = 'asc';

  constructor(private tradeService: TradeService, private router: Router) {}

  ngOnInit(): void {
    this.loading = true;
    this.tradeService.getHoldings_all().subscribe(
      data => {
        this.loading = false;
        this.holdings = data.Holdings;
        this.filteredHoldings = [...this.holdings];
      },
      error => {
        this.loading = false;
        this.error = 'Failed to load holdings, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  filterHoldings(): void {
    this.filteredHoldings = this.holdings.filter(holding =>
      holding.Symbol.toLowerCase().includes(this.filterSymbol.toLowerCase())
    );
  }

  sortHoldings(field: string): void {
    if (this.sortField === field) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortOrder = 'asc';
    }

    this.filteredHoldings.sort((a, b) => {
      const valueA = a[field as keyof Holding];
      const valueB = b[field as keyof Holding];

      if (valueA < valueB) {
        return this.sortOrder === 'asc' ? -1 : 1;
      } else if (valueA > valueB) {
        return this.sortOrder === 'asc' ? 1 : -1;
      } else {
        return 0;
      }
    });
  }

  call_squareoff(holding: Holding): void {
    const positionData = JSON.stringify(holding);
    this.router.navigate(['/square-off-position', { position: positionData }]);
  }
}