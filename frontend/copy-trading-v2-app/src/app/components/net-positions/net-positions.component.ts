import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { NetPositionResponse, Position } from './position.model';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-net-positions',
  templateUrl: './net-positions.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule, FormsModule]
})
export class NetPositionsComponent implements OnInit {
  positions: Position[] = [];
  filteredPositions: Position[] = [];
  error: string | null = null;
  loading: boolean = false;
  filterSymbol: string = '';
  sortField: string = '';
  sortOrder: string = 'asc';

  constructor(private tradeService: TradeService, private router: Router) {}

  ngOnInit(): void {
    this.loading = true;
    this.tradeService.getNetPositions().subscribe(
      (data: NetPositionResponse) => {
        this.loading = false;
        if (data && data.Positions) {
          this.positions = data.Positions;
          this.filteredPositions = [...this.positions];
        } else {
          console.error("Data format is incorrect");
        }
      },
      error => {
        this.loading = false;
        this.error = 'Failed to load Net Positions, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  filterPositions(): void {
    this.filteredPositions = this.positions.filter(position =>
      position.Symbol.toLowerCase().includes(this.filterSymbol.toLowerCase())
    );
  }

  sortPositions(field: string): void {
    if (this.sortField === field) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortOrder = 'asc';
    }

    this.filteredPositions.sort((a, b) => {
      const valueA = a[field as keyof Position];
      const valueB = b[field as keyof Position];

      if (valueA < valueB) {
        return this.sortOrder === 'asc' ? -1 : 1;
      } else if (valueA > valueB) {
        return this.sortOrder === 'asc' ? 1 : -1;
      } else {
        return 0;
      }
    });
  }

  call_squareoff(position: Position): void {
    const positionData = JSON.stringify(position);
    this.router.navigate(['/square-off-position', { position: positionData }]);
  }
}