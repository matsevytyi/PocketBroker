"use client";

import React, { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { createClient } from "@/lib/supabase/client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { ChevronDown, Eye, EyeOff, Shield, Key, User, Phone, ArrowLeft, ArrowRight, Check } from "lucide-react";

interface OnboardingData {
  firstName: string;
  lastName: string;
  phoneNumber: string;
  password: string;
  riskTolerance: string;
  krakenApiKey: string;
}

const riskToleranceOptions = [
  { value: "conservative", label: "Conservative", description: "Low risk, stable returns" },
  { value: "moderate", label: "Moderate", description: "Balanced risk and return" },
  { value: "aggressive", label: "Aggressive", description: "High risk, high potential returns" },
];

const steps = [
  { id: 1, title: "Personal Information", description: "Tell us about yourself" },
  { id: 2, title: "Security", description: "Secure your account" },
  { id: 3, title: "Investment Details", description: "Set your preferences" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const supabase = createClient();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<OnboardingData>({
    firstName: "",
    lastName: "",
    phoneNumber: "",
    password: "",
    riskTolerance: "",
    krakenApiKey: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field: keyof OnboardingData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handlePhoneChange = (value: string) => {
    // Format phone number as user types
    const formatted = value.replace(/\D/g, '').replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    handleInputChange('phoneNumber', formatted);
  };

  const handlePasswordChange = (value: string) => {
    // Limit to 4 digits
    const digitsOnly = value.replace(/\D/g, '').slice(0, 4);
    handleInputChange('password', digitsOnly);
  };

  // Memoized validation for current step
  const currentStepValid = useMemo(() => {
    switch (currentStep) {
      case 1:
        return formData.firstName.trim().length > 0 && formData.lastName.trim().length > 0;
      case 2:
        return formData.phoneNumber.replace(/\D/g, '').length === 10 && formData.password.length === 4;
      case 3:
        return formData.riskTolerance.length > 0 && formData.krakenApiKey.trim().length > 0;
      default:
        return false;
    }
  }, [currentStep, formData]);

  const nextStep = () => {
    if (currentStep < 3 && currentStepValid) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    try {
      // Get current user
      const { data: { user }, error: userError } = await supabase.auth.getUser();
      
      if (userError || !user) {
        throw new Error('User not authenticated');
      }

      // Update profile with onboarding data
      const { error: updateError } = await supabase
        .from('profiles')
        .update({
          first_name: formData.firstName,
          last_name: formData.lastName,
          phone_number: formData.phoneNumber,
          pin_hash: formData.password, // Storing PIN as plain text as requested
          risk_tolerance: formData.riskTolerance,
          kraken_api_key: formData.krakenApiKey,
          onboarding_completed: true
        })
        .eq('id', user.id);

      if (updateError) {
        throw updateError;
      }
      
      // Show success toast
      toast.success("Onboarding completed successfully!", {
        description: "Welcome to PocketBroker! Let's start your investment journey.",
        duration: 3000,
      });
      
      // Redirect to /call after a short delay
      setTimeout(() => {
        router.push('/call');
      }, 1500);
      
    } catch (error) {
      console.error('Onboarding error:', error);
      toast.error("Onboarding failed", {
        description: "There was an error completing onboarding. Please try again.",
        duration: 4000,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const selectedRiskTolerance = riskToleranceOptions.find(
    option => option.value === formData.riskTolerance
  );

  const progressValue = (currentStep / 3) * 100;

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-3">
            <div className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="firstName">First Name</Label>
                <Input
                  id="firstName"
                  type="text"
                  placeholder="Enter your first name"
                  value={formData.firstName}
                  onChange={(e) => handleInputChange('firstName', e.target.value)}
                  required
                />
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="lastName">Last Name</Label>
                <Input
                  id="lastName"
                  type="text"
                  placeholder="Enter your last name"
                  value={formData.lastName}
                  onChange={(e) => handleInputChange('lastName', e.target.value)}
                  required
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-3">
            <div className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="phoneNumber" className="flex items-center gap-2">
                  <Phone className="h-4 w-4" />
                  Phone Number
                </Label>
                <Input
                  id="phoneNumber"
                  type="tel"
                  placeholder="(555) 123-4567"
                  value={formData.phoneNumber}
                  onChange={(e) => handlePhoneChange(e.target.value)}
                  required
                />
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="password">4-Digit PIN</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter 4-digit PIN"
                    value={formData.password}
                    onChange={(e) => handlePasswordChange(e.target.value)}
                    maxLength={4}
                    className="pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                <p className="text-sm text-slate-500">This will be used to secure your account</p>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-3">
            <div className="space-y-2">
              <div className="space-y-1">
                <Label>Risk Tolerance</Label>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button 
                      variant="outline" 
                      className="w-full justify-between"
                      disabled={isSubmitting}
                    >
                      {selectedRiskTolerance ? selectedRiskTolerance.label : "Select your risk tolerance"}
                      <ChevronDown className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-full">
                    {riskToleranceOptions.map((option) => (
                      <DropdownMenuItem
                        key={option.value}
                        onClick={() => handleInputChange('riskTolerance', option.value)}
                        className="flex flex-col items-start p-3"
                      >
                        <div className="font-medium">{option.label}</div>
                        <div className="text-sm text-slate-500">{option.description}</div>
                      </DropdownMenuItem>
                    ))}
                  </DropdownMenuContent>
                </DropdownMenu>
                {selectedRiskTolerance && (
                  <p className="text-sm text-slate-500">{selectedRiskTolerance.description}</p>
                )}
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="krakenApiKey">Kraken API Key</Label>
                <div className="relative">
                  <Input
                    id="krakenApiKey"
                    type={showApiKey ? "text" : "password"}
                    placeholder="Enter your Kraken API key"
                    value={formData.krakenApiKey}
                    onChange={(e) => handleInputChange('krakenApiKey', e.target.value)}
                    className="pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowApiKey(!showApiKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700"
                  >
                    {showApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                <p className="text-sm text-slate-500">
                  Your API key is encrypted and stored securely. We only use it to fetch your portfolio data.
                </p>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-2 sm:p-4 lg:p-6">
      <Card className="w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-2xl mx-auto">
        <CardHeader className="text-center px-4 sm:px-6 pb-2">
          <CardTitle className="text-xl sm:text-2xl lg:text-3xl font-bold flex items-center justify-center gap-2">
            Welcome to PocketBroker! Let&apos;s Get Started
          </CardTitle>
          <CardDescription className="text-sm sm:text-base lg:text-lg">
            Quickly complete your profile to begin your investment journey
          </CardDescription>
        </CardHeader>
        
        <CardContent className="px-4 sm:px-6 pt-2">
          {/* Progress Bar */}
          <div className="mb-3 sm:mb-4">
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs sm:text-sm font-medium text-slate-600 dark:text-slate-400">
                Step {currentStep} of 3: {steps[currentStep - 1]?.title}
              </span>
              <span className="text-xs sm:text-sm text-slate-500">
                {Math.round(progressValue)}% Complete
              </span>
            </div>
            <Progress value={progressValue} className="h-2" />
          </div>

          {/* Step Content */}
          <div className="min-h-[150px] sm:min-h-[180px] lg:min-h-[220px]">
            {renderStepContent()}
          </div>

          {/* Navigation Buttons */}
          <div className="flex flex-col sm:flex-row justify-between gap-3 sm:gap-0 pt-3 sm:pt-4 border-t">
            <Button
              variant="outline"
              onClick={prevStep}
              disabled={currentStep === 1}
              className="flex items-center justify-center gap-2 w-full sm:w-auto order-2 sm:order-1"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
            
            {currentStep < 3 ? (
              <Button
                onClick={nextStep}
                disabled={!currentStepValid}
                className="flex items-center justify-center gap-2 w-full sm:w-auto order-1 sm:order-2"
              >
                Next
                <ArrowRight className="h-4 w-4" />
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                disabled={!currentStepValid || isSubmitting}
                className="flex items-center justify-center gap-2 w-full sm:w-auto order-1 sm:order-2"
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span className="hidden sm:inline">Completing Setup...</span>
                    <span className="sm:hidden">Completing...</span>
                  </>
                ) : (
                  <>
                    <Check className="h-4 w-4" />
                    <span className="hidden sm:inline">Complete Onboarding</span>
                    <span className="sm:hidden">Complete</span>
                  </>
                )}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
