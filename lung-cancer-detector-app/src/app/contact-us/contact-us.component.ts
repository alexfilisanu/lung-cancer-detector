import { Component } from '@angular/core';
import { CommonModule } from "@angular/common";
import { FormControl, FormGroup, FormsModule, Validators } from "@angular/forms";
import { NgxTranslateModule } from "../translate/translate.module";

@Component({
  selector: 'app-contact-us',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    NgxTranslateModule
  ],
  templateUrl: './contact-us.component.html',
  styleUrl: './contact-us.component.css'
})
export class ContactUsComponent {
  public contactUsForm: FormGroup;

  constructor() {
    this.contactUsForm = new FormGroup({
      name: new FormControl(Validators.required),
      phone: new FormControl(Validators.required),
      email: new FormControl(Validators.required),
      message: new FormControl(Validators.required)
    });
  }
}
